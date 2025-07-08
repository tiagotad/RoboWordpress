# ROBÔ PILLOTO V4 - COM GERAÇÃO DE IMAGENS DALL·E 3
# Versão avançada que gera imagens para cada post e define como imagem em destaque

import sys
import os
import requests
import time
import base64
from io import BytesIO
from datetime import datetime
from openai import OpenAI
from requests.auth import HTTPBasicAuth
import gspread
from google.oauth2.service_account import Credentials
from PIL import Image
import json

# Importação condicional de configuração (local ou cloud)
try:
    import streamlit as st
    if hasattr(st, "secrets") and "WP_URL" in st.secrets:
        from config_cloud import *
    else:
        from config import *
except ImportError:
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

from prompt_manager import get_prompt_completo, get_system_prompt

# Inicializar cliente OpenAI com configurações atualizadas
client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=120.0,  # Timeout maior para geração de imagens e artigos
    max_retries=2   # Máximo 2 tentativas automáticas
)

print("\n--- ROBÔ PILLOTO V4 - COM GERAÇÃO DE IMAGENS DALL·E 3 ---")
print("[INFO] ✨ Esta versão gera imagens automaticamente para cada post!")

def log_with_timestamp(message):
    """Adiciona timestamp aos logs"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def gerar_prompt_imagem(titulo, conteudo_resumo):
    """Gera um prompt otimizado para DALL·E 3 baseado no título e conteúdo do artigo"""
    
    # Criar um resumo do conteúdo para o prompt da imagem
    palavras_chave = titulo.lower()
    
    # Prompt base para diferentes temas
    if any(palavra in palavras_chave for palavra in ['filme', 'cinema', 'ator', 'atriz', 'diretor']):
        prompt_base = f"Create a cinematic, movie-themed illustration representing: {titulo}. Style: modern, vibrant, professional movie poster aesthetic"
    elif any(palavra in palavras_chave for palavra in ['série', 'tv', 'netflix', 'streaming']):
        prompt_base = f"Create a modern TV series poster illustration for: {titulo}. Style: Netflix-style promotional artwork, dark and dramatic"
    elif any(palavra in palavras_chave for palavra in ['viagem', 'turismo', 'destino', 'lugar']):
        prompt_base = f"Create a beautiful travel destination illustration for: {titulo}. Style: vibrant, inspiring travel photography aesthetic"
    elif any(palavra in palavras_chave for palavra in ['tecnologia', 'tech', 'ai', 'inteligência']):
        prompt_base = f"Create a futuristic technology illustration for: {titulo}. Style: modern tech, blue and purple gradients, clean design"
    elif any(palavra in palavras_chave for palavra in ['saúde', 'exercício', 'fitness', 'bem-estar']):
        prompt_base = f"Create a health and wellness illustration for: {titulo}. Style: clean, inspiring, modern healthcare aesthetic"
    elif any(palavra in palavras_chave for palavra in ['livro', 'literatura', 'autor', 'leitura']):
        prompt_base = f"Create a literary-themed illustration for: {titulo}. Style: elegant, bookish, warm and inviting"
    else:
        # Prompt genérico para outros temas
        prompt_base = f"Create a professional, engaging illustration for the blog post: {titulo}. Style: modern, clean, visually appealing"
    
    # Adicionar especificações técnicas
    prompt_final = f"""{prompt_base}. 
    Requirements: 
    - High quality, professional artwork
    - Suitable for blog featured image
    - No text or watermarks
    - 16:9 aspect ratio preferred
    - Bright, engaging colors
    - Modern and clean aesthetic"""
    
    return prompt_final

def gerar_imagem_dalle(prompt_imagem, titulo):
    """Gera uma imagem usando DALL·E 3"""
    print(f"[INFO] 🎨 Gerando imagem para: {titulo}")
    print(f"[INFO] Prompt da imagem: {prompt_imagem[:100]}...")
    
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_imagem,
            size="1792x1024",  # Formato wide para featured image
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        print(f"[✔] Imagem gerada com sucesso: {image_url}")
        return image_url
        
    except Exception as e:
        print(f"[ERRO] Falha ao gerar imagem: {e}")
        return None

def baixar_imagem(image_url, nome_arquivo):
    """Baixa a imagem gerada pelo DALL·E 3"""
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # Salvar imagem temporariamente
        with open(nome_arquivo, 'wb') as f:
            f.write(response.content)
        
        print(f"[✔] Imagem salva como: {nome_arquivo}")
        return True
        
    except Exception as e:
        print(f"[ERRO] Falha ao baixar imagem: {e}")
        return False

def upload_imagem_wordpress(caminho_imagem, titulo, alt_text):
    """Faz upload da imagem para o WordPress e retorna o ID da mídia"""
    try:
        print(f"[INFO] 📤 Fazendo upload da imagem para WordPress...")
        
        # Endpoint para upload de mídia
        media_endpoint = f"{WP_URL}/wp-json/wp/v2/media"
        
        # Preparar arquivo para upload
        with open(caminho_imagem, 'rb') as img_file:
            files = {
                'file': (f"{titulo}.jpg", img_file, 'image/jpeg')
            }
            
            headers = {
                'Content-Disposition': f'attachment; filename="{titulo}.jpg"'
            }
            
            data = {
                'title': titulo,
                'alt_text': alt_text,
                'caption': f'Imagem gerada para: {titulo}'
            }
            
            response = requests.post(
                media_endpoint,
                files=files,
                data=data,
                headers=headers,
                auth=HTTPBasicAuth(WP_USER, WP_PASSWORD),
                timeout=60
            )
            
            response.raise_for_status()
            media_data = response.json()
            media_id = media_data['id']
            
            print(f"[✔] Imagem enviada com sucesso! ID: {media_id}")
            return media_id
            
    except Exception as e:
        print(f"[ERRO] Falha no upload da imagem: {e}")
        return None

def definir_imagem_destaque(post_id, media_id):
    """Define a imagem como featured image do post"""
    try:
        print(f"[INFO] 🖼️ Definindo imagem {media_id} como destaque do post {post_id}...")
        
        # Endpoint para atualizar post
        post_endpoint = f"{WP_URL}/wp-json/wp/v2/posts/{post_id}"
        
        data = {
            'featured_media': media_id
        }
        
        response = requests.post(
            post_endpoint,
            json=data,
            auth=HTTPBasicAuth(WP_USER, WP_PASSWORD),
            timeout=30
        )
        
        response.raise_for_status()
        print(f"[✔] Imagem definida como destaque com sucesso!")
        return True
        
    except Exception as e:
        print(f"[ERRO] Falha ao definir imagem como destaque: {e}")
        return False

# === CARREGAR TÓPICOS ===
print("\n--- CARREGANDO TÓPICOS ---")

def carregar_topicos_sheets():
    try:
        print("Configurando credenciais...")
        scope = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        if not os.path.exists(CREDENTIALS_FILE):
            raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}")
        
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
        gc = gspread.authorize(creds)
        
        print("Abrindo planilha...")
        sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        print("Lendo tópicos das células A2 até A4...")
        topicos = []
        for row in range(2, 5):
            try:
                cell_value = sheet.cell(row, 1).value
                if cell_value and cell_value.strip():
                    topicos.append(cell_value.strip())
                    print(f"  Tópico encontrado na linha {row}: {cell_value.strip()}")
            except Exception as e:
                print(f"[AVISO] Erro ao ler linha {row}: {e}")
                continue
        
        return topicos
        
    except Exception as e:
        print(f"[ERRO] Não foi possível carregar tópicos do Google Sheets: {e}")
        return []

topicos = carregar_topicos_sheets()

# Usar tópicos da configuração ao invés da planilha
topicos_config = config_execucao.get('topicos_lista', [])
if topicos_config:
    topicos = topicos_config
    print(f"[INFO] Usando {len(topicos)} tópicos da configuração da interface")

quantidade_maxima = config_execucao.get('quantidade_textos', 3)
print(f"[INFO] Quantidade de textos por tópico (config): {quantidade_maxima}")
# Não limitar a lista de tópicos aqui! A lista já vem expandida do frontend.

print("Tópicos que serão processados:")
for i, t in enumerate(topicos, 1):
    print(f" {i}. {t}")

print("\n[INFO] *** VERSÃO V4 - AGORA COM GERAÇÃO DE IMAGENS AUTOMÁTICA! ***")

# === GERAR CONTEÚDO + IMAGENS ===
for idx, topico_geral in enumerate(topicos, 1):
    log_with_timestamp(f"--- PROCESSANDO TÓPICO {idx}/{len(topicos)}: {topico_geral} ---")
    log_with_timestamp(f"[LOG] Iniciando geração de conteúdo para o tópico: {topico_geral}")
    try:
        # === GERAR TÍTULO E ARTIGO COM PROMPT ÚNICO ===
        log_with_timestamp("[INFO] 📝 Carregando prompt personalizado completo...")
        prompt_completo = get_prompt_completo(topico_geral)
        system_prompt = get_system_prompt()

        response_completo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_completo}
            ],
            temperature=0.7,
            max_tokens=4000
        )

        # Processar resposta completa
        resposta_completa = response_completo.choices[0].message.content.strip()
        
        # Extrair título e artigo da resposta
        try:
            # Procurar por padrões de título
            if "TÍTULO:" in resposta_completa:
                partes = resposta_completa.split("TÍTULO:", 1)[1].split("ARTIGO:", 1)
                titulo_especifico = partes[0].strip()
                conteudo = partes[1].strip() if len(partes) > 1 else ""
            elif resposta_completa.startswith("#"):
                # Se começar com #, primeira linha é título
                linhas = resposta_completa.split("\n", 1)
                titulo_especifico = linhas[0].strip("# ").strip()
                conteudo = linhas[1].strip() if len(linhas) > 1 else ""
            else:
                # Tentar extrair título da primeira linha
                linhas = resposta_completa.split("\n", 1)
                titulo_especifico = linhas[0].strip()
                conteudo = linhas[1].strip() if len(linhas) > 1 else resposta_completa
            
            # Validar se extraiu corretamente
            if not titulo_especifico or not conteudo:
                raise ValueError("Não foi possível extrair título ou conteúdo da resposta")
                
            log_with_timestamp(f"[LOG] ✅ Título extraído: {titulo_especifico}")
            log_with_timestamp(f"[LOG] ✅ Artigo gerado ({len(conteudo)} caracteres)")
            
        except Exception as e:
            log_with_timestamp(f"[AVISO] Erro ao processar resposta: {e}")
            log_with_timestamp("[INFO] Usando resposta completa como artigo e gerando título simples")
            titulo_especifico = f"Artigo sobre {topico_geral}"
            conteudo = resposta_completa

        log_with_timestamp(f"[LOG] ✅ Conteúdo gerado para '{titulo_especifico}' (tópico: {topico_geral})")
        log_with_timestamp(f"[EXEMPLO] Início do artigo: {conteudo[:200]}...")

        # === GERAR IMAGEM COM DALL·E 3 ===
        log_with_timestamp("[LOG] 🎨 Gerando imagem com DALL·E 3...")
        
        # Criar prompt para imagem baseado no título e conteúdo
        prompt_imagem = gerar_prompt_imagem(titulo_especifico, conteudo[:500])
        
        # Gerar imagem
        image_url = gerar_imagem_dalle(prompt_imagem, titulo_especifico)
        
        media_id = None
        nome_arquivo_img = None
        
        if image_url:
            # Baixar imagem
            nome_arquivo_img = f"imagem_{titulo_especifico[:30].replace(' ', '_').replace('/', '_')}.jpg"
            nome_arquivo_img = "".join(c for c in nome_arquivo_img if c.isalnum() or c in "._-")
            
            if baixar_imagem(image_url, nome_arquivo_img):
                # Upload para WordPress
                alt_text = f"Imagem representando: {titulo_especifico}"
                media_id = upload_imagem_wordpress(nome_arquivo_img, titulo_especifico, alt_text)
        
        # === BUSCAR/CRIAR CATEGORIA ===
        categoria_config = config_execucao.get('categoria_wp', 32174)  # Padrão: 32174 (mundo)
        
        try:
            # Se categoria_config é um número, usar como ID diretamente
            if isinstance(categoria_config, (int, str)) and str(categoria_config).isdigit():
                category_id = int(categoria_config)
                print(f"[INFO] Usando categoria ID: {category_id}")
                
                # Verificar se a categoria existe (opcional)
                try:
                    category_check = requests.get(f"{WP_URL}/wp-json/wp/v2/categories/{category_id}", 
                                                auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
                    if category_check.status_code == 200:
                        category_name = category_check.json().get('name', f'ID {category_id}')
                        print(f"[INFO] Categoria verificada: '{category_name}' (ID: {category_id})")
                    else:
                        print(f"[AVISO] Categoria ID {category_id} pode não existir, mas tentando usar mesmo assim")
                except:
                    print(f"[INFO] Não foi possível verificar categoria ID {category_id}, mas prosseguindo")
                    
            else:
                # Se categoria_config é texto, buscar por nome (comportamento antigo)
                categoria_desejada = str(categoria_config)
                print(f"[INFO] Buscando categoria por nome: '{categoria_desejada}'")
                
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
                    print(f"[INFO] Categoria '{categoria_desejada}' criada com ID: {category_id}")
                else:
                    print(f"[INFO] Usando categoria existente '{categoria_desejada}' com ID: {category_id}")
            
        except Exception as e:
            print(f"[AVISO] Erro ao processar categoria: {e}")
            print(f"[INFO] Usando categoria padrão ID: 32174")
            category_id = 32174

        # === PUBLICAR NO WORDPRESS ===

        # === PUBLICAR NO WORDPRESS COM AUTOR ===
        status_publicacao = config_execucao.get('status_publicacao', 'draft')
        author_id = config_execucao.get('author_id', 1)
        post_data = {
            'title': titulo_especifico,
            'content': conteudo,
            'status': status_publicacao,
            'categories': [category_id],
            'author': author_id
        }
        # Adicionar imagem em destaque se foi gerada
        if media_id:
            post_data['featured_media'] = media_id

        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        response_wp = requests.post(endpoint, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=20)
        response_wp.raise_for_status()
        
        post_data_response = response_wp.json()
        post_id = post_data_response['id']

        status_msg = "publicado" if status_publicacao == "publish" else "salvo como rascunho"
        log_with_timestamp(f"[✔] Post {status_msg} com sucesso na categoria ID {category_id} (autor ID {author_id}): {titulo_especifico}")
        log_with_timestamp(f"[RESULTADO] Post publicado com sucesso! ID: {post_id}")
        log_with_timestamp(f"[INFO] URL do post: {WP_URL}/?p={post_id}")
        
        if media_id:
            log_with_timestamp(f"[✔] 🖼️ Imagem em destaque definida com sucesso!")
        else:
            log_with_timestamp(f"[⚠️] Post criado sem imagem em destaque (erro na geração)")
        
        log_with_timestamp(f"[INFO] Usando prompts personalizados + DALL·E 3")
        
        # Limpar arquivo temporário
        if nome_arquivo_img and os.path.exists(nome_arquivo_img):
            try:
                os.remove(nome_arquivo_img)
                print(f"[INFO] Arquivo temporário removido: {nome_arquivo_img}")
            except:
                pass

    except Exception as e:
        log_with_timestamp(f"[ERRO] Falha ao processar tópico '{topico_geral}': {e}")
        # ...existing code...

    print(f"[INFO] ⏱️ Aguardando 15 segundos antes do próximo post...")
    time.sleep(15)  # Tempo maior entre posts devido à geração de imagens

print("\n--- FINALIZADO COM SUCESSO ---")
print("[INFO] 🎯 Para editar os prompts, use a interface web: streamlit run app.py")
print("[INFO] ✨ Versão V4 - Agora com imagens automáticas geradas por DALL·E 3!")
