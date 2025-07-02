# -*- coding: utf-8 -*-

# Bloco robusto para garantir importação do config.py
import sys
import os
project_root_candidates = [
    os.path.dirname(os.path.abspath(__file__)),
    os.getcwd(),
    '/mount/src/robowordpress'
]
for path in project_root_candidates:
    if path not in sys.path and os.path.exists(os.path.join(path, 'config.py')):
        sys.path.insert(0, path)
        break
else:
    for path in project_root_candidates:
        if path not in sys.path:
            sys.path.insert(0, path)

import requests
import time
import json
import gspread
from openai import OpenAI
from requests.auth import HTTPBasicAuth
from oauth2client.service_account import ServiceAccountCredentials
from config import *

# Validar configurações ao iniciar
if not validar_configuracoes():
    exit(1)

# 2. Carrega tópicos do Google Sheets
def carregar_topicos():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_JSON, scope)
    client = gspread.authorize(creds)
    sheet = client.open(GOOGLE_SHEET_NAME).sheet1
    topicos = sheet.col_values(1)[1:]  # Pega coluna A ignorando cabeçalho
    return topicos

# 3. Inicializa cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

print("--- INICIANDO ROBÔ SEO PARA WORDPRESS ---")

# 4. Loop de geração e publicação
for topico in carregar_topicos():
    print(f"\n[1/3] Gerando conteúdo para o tópico: '{topico}'")

    try:
        # Prompt estruturado para retorno JSON SEO
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a blog assistant that writes SEO-optimized blog posts in English for an American audience. Return a JSON with: title, description, tags (list), content."
                },
                {
                    "role": "user",
                    "content": f"""Write a blog post of around 800 words on the topic: '{topico}'.
Make sure it includes:
- SEO title (max 60 characters)
- Meta description (max 160 characters)
- 5 to 8 SEO tags
- Blog content in markdown

Return in JSON format:
{{
  "title": "...",
  "description": "...",
  "tags": ["tag1", "tag2", ...],
  "content": "..."
}}"""
                }
            ]
        )

        resposta_json = json.loads(response.choices[0].message.content)

        title = resposta_json["title"]
        description = resposta_json["description"]
        tags = resposta_json["tags"]
        content = resposta_json["content"]

        print("[2/3] Conteúdo gerado com sucesso. Publicando no WordPress...")

        # Dados para o WordPress
        post_data = {
            'title': title,
            'excerpt': description,
            'content': content,
            'status': 'publish'
        }

        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        response_wp = requests.post(endpoint, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=20)
        response_wp.raise_for_status()

        print(f"[3/3] SUCESSO! Artigo '{title}' publicado com sucesso.")

    except json.JSONDecodeError:
        print(f"[ERRO] A IA não retornou um JSON válido para o tópico '{topico}'")
    except requests.exceptions.RequestException as e:
        print(f"[ERRO NO WORDPRESS] Erro ao publicar '{topico}': {e}")
    except Exception as e:
        print(f"[ERRO GERAL] Tópico '{topico}' falhou com erro: {e}")

    time.sleep(10)

print("\n--- TODOS OS ARTIGOS PROCESSADOS ---")