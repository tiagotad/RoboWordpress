# 1. Importar as bibliotecas necessárias

import sys
import os
import requests
import time
from openai import OpenAI
from requests.auth import HTTPBasicAuth
import gspread
from google.oauth2.service_account import Credentials

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
except ImportError:
    print("[AVISO] Arquivo config_execucao.py não encontrado, usando configurações padrão")
    config_execucao = {
        'categoria_wp': 'Others',
        'status_publicacao': 'draft',
        'quantidade_textos': 3
    }

from prompt_manager import get_prompt_titulo, get_prompt_artigo, get_system_prompts

# Validar configurações ao iniciar

# Inicializar cliente OpenAI com configurações atualizadas
client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=30.0,  # Timeout de 30 segundos
    max_retries=3   # Máximo 3 tentativas
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
    print(f"[INFO] Usando {len(topicos)} tópicos da configuração da interface")

quantidade_maxima = config_execucao.get('quantidade_textos', 3)
print(f"[INFO] Quantidade de textos por tópico (config): {quantidade_maxima}")
# Não limitar a lista de tópicos aqui! A lista já vem expandida do frontend.

print("Tópicos que serão processados:")
for i, t in enumerate(topicos, 1):
    print(f" {i}. {t}")

print("\n[INFO] *** TÓPICOS AGORA VÊM DA INTERFACE WEB - Google Sheets não é mais necessário ***")

# === GERAR TÍTULOS E ARTIGOS BASEADOS NOS TÓPICOS DA INTERFACE ===
for idx, topico_geral in enumerate(topicos, 1):
    print(f"\n--- PROCESSANDO TÓPICO {idx}/{len(topicos)}: {topico_geral} ---")
    print(f"[LOG] Iniciando geração de título para o tópico: {topico_geral}")
    try:
        # === GERAR TÍTULO ESPECÍFICO BASEADO NO TÓPICO GERAL ===
        print("[INFO] Carregando prompt personalizado para título...")
        prompt_titulo = get_prompt_titulo(topico_geral)
        system_prompts = get_system_prompts()

        response_titulo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompts['titulo']},
                {"role": "user", "content": prompt_titulo}
            ],
            temperature=0.8,  # Mais criatividade para títulos cativantes
            max_tokens=120
        )

        titulo_especifico = response_titulo.choices[0].message.content.strip().strip('"')
        print(f"[LOG] Título gerado para '{topico_geral}': {titulo_especifico}")
        print(f"[EXEMPLO] Título retornado: {titulo_especifico}")

        # === GERAR ARTIGO BASEADO EM PESQUISA ===
        print(f"[LOG] Iniciando geração do artigo para o título: {titulo_especifico}")
        print("[INFO] Carregando prompt personalizado para artigo...")
        prompt_artigo = get_prompt_artigo(titulo_especifico, topico_geral)

        response_artigo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompts['artigo']},
                {"role": "user", "content": prompt_artigo}
            ],
            temperature=0.7,
            max_tokens=3000
        )

        conteudo = response_artigo.choices[0].message.content.strip()
        print(f"[LOG] Artigo gerado para '{titulo_especifico}' (tópico: {topico_geral})")
        print(f"[EXEMPLO] Início do artigo: {conteudo[:200]} ...\n---fim do preview---\n")

        # === PUBLICAR POST ===
        print(f"[LOG] Publicando post '{titulo_especifico}' no WordPress...")
        # ... código de publicação ...
        # Exemplo de resultado:
        # print(f"[RESULTADO] Post publicado com sucesso! URL: https://seusite.com/{slug}")

    except Exception as e:
        print(f"[ERRO] Falha ao processar tópico '{topico_geral}': {e}")

    time.sleep(10)  # Evita bloqueios na API do WordPress

print("\n--- FINALIZADO COM SUCESSO ---")
print("[INFO] 🎯 Para editar os prompts, use a interface web: streamlit run app.py")
