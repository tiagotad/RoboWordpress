# 1. Importar as bibliotecas necessárias

import sys
import os
import requests
import time
from datetime import datetime
from openai import OpenAI
from requests.auth import HTTPBasicAuth
import gspread
from google.oauth2.service_account import Credentials

# Importação condicional de configuração (local ou cloud)
try:
    import streamlit as st
    # Só tentar acessar secrets se estiver em contexto do Streamlit
    if hasattr(st, "secrets") and hasattr(st.secrets, "_secrets") and "WP_URL" in st.secrets:
        from config_cloud import *
    else:
        from config import *
except (ImportError, Exception):
    # Se der qualquer erro (incluindo StreamlitSecretNotFoundError), usar config local
    from config import *

# Importar configurações de execução
try:
    from config_execucao import get_configuracoes_execucao
    config_execucao = get_configuracoes_execucao()
    print(f"[INFO] Configurações de execução: {config_execucao}")
    
    # Se as credenciais WordPress estão no config_execucao, usar essas
    if 'wp_url' in config_execucao and 'wp_user' in config_execucao and 'wp_password' in config_execucao:
        WP_URL = config_execucao['wp_url']
        WP_USER = config_execucao['wp_user'] 
        WP_PASSWORD = config_execucao['wp_password']
        print(f"[INFO] ✅ Usando credenciais WordPress da interface: {WP_URL}")
    else:
        print(f"[INFO] ⚠️ Usando credenciais WordPress do arquivo config.py")
        
except ImportError:
    print("[AVISO] Arquivo config_execucao.py não encontrado, usando configurações padrão")
    config_execucao = {
        'categoria_wp': 'Others',
        'status_publicacao': 'draft',
        'quantidade_textos': 3
    }

from prompt_manager import get_prompt_titulo, get_prompt_artigo, get_system_prompts

# Função para log com timestamp
def log_with_timestamp(message):
    """Adiciona timestamp aos logs"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

# Validar configurações ao iniciar

# Inicializar cliente OpenAI com configurações atualizadas
client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=120.0,  # Timeout padrão de 2 minutos
    max_retries=2   # Máximo 2 tentativas automáticas (além das nossas manuais)
)

print("\n--- CARREGANDO TÓPICOS DO GOOGLE SHEETS ---")

# === CARREGAR TÓPICOS DO GOOGLE SHEETS ===
def carregar_topicos_sheets():
    try:
        print("Configurando credenciais...")
        # Configurar credenciais do Google Sheets
        scope = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        # Verificar se o arquivo de credenciais existe
        if not os.path.exists(CREDENTIALS_FILE):
            raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}")
        
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
        gc = gspread.authorize(creds)
        
        print("Abrindo planilha...")
        # Abrir a planilha
        sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        print("Lendo tópicos das células A2 até A4...")
        # Ler valores das células A2 até A4
        topicos = []
        for row in range(2, 5):  # Linhas 2, 3, 4
            try:
                cell_value = sheet.cell(row, 1).value  # Coluna A
                if cell_value and cell_value.strip():
                    topicos.append(cell_value.strip())
                    print(f"  Tópico encontrado na linha {row}: {cell_value.strip()}")
            except Exception as e:
                print(f"[AVISO] Erro ao ler linha {row}: {e}")
                continue
        
        return topicos
        
    except Exception as e:
        print(f"[ERRO] Não foi possível carregar tópicos do Google Sheets: {e}")
        print(f"Detalhes do erro: {type(e).__name__}")
        return []

topicos = carregar_topicos_sheets()

# Usar tópicos da configuração ao invés da planilha
topicos_config = config_execucao.get('topicos_lista', [])
if topicos_config:
    topicos = topicos_config
    print(f"[INFO] ✅ Usando {len(topicos)} tópicos da configuração da interface")
    print(f"[DEBUG] Tópicos carregados: {topicos[:5]}{'...' if len(topicos) > 5 else ''}")
else:
    print(f"[INFO] ⚠️ Configuração de tópicos não encontrada, usando {len(topicos)} tópicos do Google Sheets")

print(f"[INFO] 📊 Total de tópicos para processar: {len(topicos)}")
if not topicos:
    print("[ERRO] ❌ Nenhum tópico encontrado! Verifique a configuração.")
    sys.exit(1)

quantidade_maxima = config_execucao.get('quantidade_textos', 3)
print(f"[INFO] Quantidade de textos por tópico (config): {quantidade_maxima}")
# Não limitar a lista de tópicos aqui! A lista já vem expandida do frontend.

print("Tópicos que serão processados:")
for i, t in enumerate(topicos, 1):
    print(f" {i}. {t}")

print("\n[INFO] *** TÓPICOS AGORA VÊM DA INTERFACE WEB - Google Sheets não é mais necessário ***")

# === GERAR TÍTULOS E ARTIGOS BASEADOS NOS TÓPICOS DA INTERFACE ===
posts_criados = 0
posts_falharam = 0

for idx, topico_geral in enumerate(topicos, 1):
    log_with_timestamp(f"--- PROCESSANDO TÓPICO {idx}/{len(topicos)}: {topico_geral} ---")
    log_with_timestamp(f"[LOG] Iniciando geração de título para o tópico: {topico_geral}")
    try:
        # === GERAR TÍTULO ESPECÍFICO BASEADO NO TÓPICO GERAL ===
        log_with_timestamp("[INFO] Carregando prompt personalizado para título...")
        prompt_titulo = get_prompt_titulo(topico_geral)
        system_prompts = get_system_prompts()

        # Retry para geração de título
        max_retries = 3
        for tentativa in range(max_retries):
            try:
                log_with_timestamp(f"[LOG] Tentativa {tentativa + 1}/{max_retries} - Gerando título...")
                response_titulo = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompts['titulo']},
                        {"role": "user", "content": prompt_titulo}
                    ],
                    temperature=0.8,  # Mais criatividade para títulos cativantes
                    max_tokens=120,
                    timeout=45  # Timeout específico de 45 segundos
                )
                break  # Se chegou aqui, deu certo
            except Exception as e:
                log_with_timestamp(f"[AVISO] Tentativa {tentativa + 1} falhou para título: {e}")
                if tentativa == max_retries - 1:
                    raise Exception(f"Falha após {max_retries} tentativas na geração do título: {e}")
                time.sleep(5)  # Aguardar antes de tentar novamente

        titulo_especifico = response_titulo.choices[0].message.content.strip().strip('"')
        log_with_timestamp(f"[LOG] ✅ Título gerado para '{topico_geral}': {titulo_especifico}")
        log_with_timestamp(f"[EXEMPLO] Título retornado: {titulo_especifico}")

        # === GERAR ARTIGO BASEADO EM PESQUISA ===
        log_with_timestamp(f"[LOG] Iniciando geração do artigo para o título: {titulo_especifico}")
        log_with_timestamp("[INFO] Carregando prompt personalizado para artigo...")
        prompt_artigo = get_prompt_artigo(titulo_especifico, topico_geral)

        # Retry para geração de artigo
        for tentativa in range(max_retries):
            try:
                log_with_timestamp(f"[LOG] Tentativa {tentativa + 1}/{max_retries} - Gerando artigo (pode levar até 60s)...")
                response_artigo = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": system_prompts['artigo']},
                        {"role": "user", "content": prompt_artigo}
                    ],
                    temperature=0.7,
                    max_tokens=3000,
                    timeout=90  # Timeout maior para artigos (90 segundos)
                )
                break  # Se chegou aqui, deu certo
            except Exception as e:
                log_with_timestamp(f"[AVISO] Tentativa {tentativa + 1} falhou para artigo: {e}")
                if tentativa == max_retries - 1:
                    raise Exception(f"Falha após {max_retries} tentativas na geração do artigo: {e}")
                log_with_timestamp(f"[INFO] Aguardando 10 segundos antes da próxima tentativa...")
                time.sleep(10)  # Aguardar mais tempo entre tentativas de artigo

        conteudo = response_artigo.choices[0].message.content.strip()
        log_with_timestamp(f"[LOG] ✅ Artigo gerado para '{titulo_especifico}' (tópico: {topico_geral})")
        log_with_timestamp(f"[EXEMPLO] Início do artigo: {conteudo[:200]}...")

        # === PUBLICAR POST ===
        log_with_timestamp(f"[LOG] Publicando post '{titulo_especifico}' no WordPress...")
        
        # Buscar categoria desejada (agora suporta ID numérico ou nome)
        categoria_config = config_execucao.get('categoria_wp', 32174)  # Padrão: 32174 (mundo)
        
        try:
            # Se categoria_config é um número, usar como ID diretamente
            if isinstance(categoria_config, (int, str)) and str(categoria_config).isdigit():
                category_id = int(categoria_config)
                log_with_timestamp(f"[INFO] Usando categoria ID: {category_id}")
                
                # Verificar se a categoria existe (opcional)
                try:
                    category_check = requests.get(f"{WP_URL}/wp-json/wp/v2/categories/{category_id}", 
                                                auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
                    if category_check.status_code == 200:
                        category_name = category_check.json().get('name', f'ID {category_id}')
                        log_with_timestamp(f"[INFO] Categoria verificada: '{category_name}' (ID: {category_id})")
                    else:
                        log_with_timestamp(f"[AVISO] Categoria ID {category_id} pode não existir, mas tentando usar mesmo assim")
                except:
                    log_with_timestamp(f"[INFO] Não foi possível verificar categoria ID {category_id}, mas prosseguindo")
                    
            else:
                # Se categoria_config é texto, buscar por nome (comportamento antigo)
                categoria_desejada = str(categoria_config)
                log_with_timestamp(f"[INFO] Buscando categoria por nome: '{categoria_desejada}'")
                
                categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
                categories_response = requests.get(categories_endpoint, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
                categories_response.raise_for_status()
                
                categories = categories_response.json()
                category_id = None
                
                for category in categories:
                    if category['name'].lower() == categoria_desejada.lower():
                        category_id = category['id']
                        break
                
                if category_id is None:
                    create_category_data = {
                        'name': categoria_desejada,
                        'slug': categoria_desejada.lower().replace(' ', '-')
                    }
                    create_response = requests.post(categories_endpoint, json=create_category_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
                    create_response.raise_for_status()
                    category_id = create_response.json()['id']
                    log_with_timestamp(f"[INFO] Categoria '{categoria_desejada}' criada com ID: {category_id}")
                else:
                    log_with_timestamp(f"[INFO] Usando categoria existente '{categoria_desejada}' com ID: {category_id}")
            
        except Exception as e:
            log_with_timestamp(f"[AVISO] Erro ao processar categoria: {e}")
            log_with_timestamp(f"[INFO] Usando categoria padrão ID: 32174")
            category_id = 32174

        # Publicar no WordPress com autor
        status_publicacao = config_execucao.get('status_publicacao', 'draft')
        author_id = config_execucao.get('author_id', 1)
        
        log_with_timestamp(f"[LOG] 📤 Iniciando publicação no WordPress...")
        log_with_timestamp(f"[INFO] Título: '{titulo_especifico}' | Status: {status_publicacao} | Autor ID: {author_id}")
        
        post_data = {
            'title': titulo_especifico,
            'content': conteudo,
            'status': status_publicacao,
            'categories': [category_id],
            'author': author_id
        }

        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        log_with_timestamp(f"[DEBUG] Enviando POST para: {endpoint}")
        
        response_wp = requests.post(endpoint, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=20)
        response_wp.raise_for_status()
        
        post_data_response = response_wp.json()
        post_id = post_data_response['id']
        post_url = post_data_response.get('link', f"{WP_URL}/?p={post_id}")

        status_msg = "publicado" if status_publicacao == "publish" else "salvo como rascunho"
        log_with_timestamp(f"[✔] Post {status_msg} com sucesso na categoria ID {category_id} (autor ID {author_id}): {titulo_especifico}")
        log_with_timestamp(f"[RESULTADO] ✅ Post publicado com sucesso! ID: {post_id}")
        log_with_timestamp(f"[INFO] 🔗 URL do post: {post_url}")
        posts_criados += 1

    except Exception as e:
        log_with_timestamp(f"[ERRO] ❌ Falha ao processar tópico '{topico_geral}': {str(e)}")
        log_with_timestamp(f"[INFO] Tipo do erro: {type(e).__name__}")
        posts_falharam += 1
        
        # Log específico para tipos de erro comuns
        if "timeout" in str(e).lower():
            log_with_timestamp(f"[DICA] 💡 Erro de timeout - a API da OpenAI pode estar sobrecarregada. Tentando próximo tópico...")
        elif "rate limit" in str(e).lower():
            log_with_timestamp(f"[DICA] 💡 Rate limit atingido - aguardando 30 segundos...")
            time.sleep(30)
        elif "connection" in str(e).lower():
            log_with_timestamp(f"[DICA] 💡 Problema de conexão - verifique sua internet...")
        
        log_with_timestamp(f"[INFO] Continuando com o próximo tópico...")
        continue

    time.sleep(10)  # Evita bloqueios na API do WordPress

# Estatísticas finais
total_processados = len(topicos)
log_with_timestamp(f"[INFO] 📊 Estatísticas finais:")
log_with_timestamp(f"[INFO] ✅ Posts criados com sucesso: {posts_criados}")
log_with_timestamp(f"[INFO] ❌ Posts que falharam: {posts_falharam}")
log_with_timestamp(f"[INFO] 📝 Total de tópicos processados: {total_processados}")
log_with_timestamp(f"[INFO] 🎯 Configuração: Categoria={config_execucao.get('categoria_wp', 'Others')}, Status={config_execucao.get('status_publicacao', 'draft')}")

if posts_criados > 0:
    log_with_timestamp(f"[INFO] 🎉 Execução bem-sucedida! {posts_criados} posts foram criados.")
else:
    log_with_timestamp(f"[AVISO] ⚠️ Nenhum post foi criado. Verifique os erros acima.")

print("\n--- FINALIZADO COM SUCESSO ---")
print("[INFO] 🎯 Para editar os prompts, use a interface web: streamlit run app.py")
