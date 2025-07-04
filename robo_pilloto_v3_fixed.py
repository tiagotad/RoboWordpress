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

# Inicializar cliente OpenAI com configurações atualizadas
client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=30.0,  # Timeout de 30 segundos
    max_retries=3   # Máximo 3 tentativas
)

print("\n--- ROBÔ PERSONALIZÁVEL V3 - TÓPICOS DA INTERFACE ---")

# Usar tópicos da configuração ao invés da planilha
topicos_config = config_execucao.get('topicos_lista', [])
if topicos_config:
    topicos = topicos_config
    print(f"[INFO] Usando {len(topicos)} tópicos da configuração da interface")
else:
    # Se não conseguir carregar, usar tópicos padrão
    topicos = [
        "Filmes e Cinema",
        "Séries de TV",
        "História e Curiosidades",
        "Viagem e Turismo",
        "Livros e Literatura"
    ]

# Obter quantidade de textos por tópico
quantidade_textos = config_execucao.get('quantidade_textos', 3)
total_posts = len(topicos) * quantidade_textos

print(f"[INFO] Configuração: {quantidade_textos} textos por tópico")
print(f"[INFO] Total de posts que serão gerados: {total_posts}")

print("Tópicos que serão processados:")
for i, t in enumerate(topicos, 1):
    print(f" {i}. {t} ({quantidade_textos} textos cada)")

print("\n[INFO] *** TÓPICOS AGORA VÊM DA INTERFACE WEB - Google Sheets não é mais necessário ***")

# === GERAR TÍTULOS E ARTIGOS BASEADOS NOS TÓPICOS DA INTERFACE ===
contador_post = 0
for indice_topico, topico_geral in enumerate(topicos, 1):
    print(f"\n{'='*80}")
    print(f"📂 TÓPICO {indice_topico}/{len(topicos)}: {topico_geral.upper()}")
    print(f"📝 Gerando {quantidade_textos} posts para este tópico")
    print(f"{'='*80}")
    
    for num_texto in range(1, quantidade_textos + 1):
        contador_post += 1
        print(f"\n--- POST {contador_post}/{total_posts} | TÓPICO: {topico_geral} | TEXTO {num_texto}/{quantidade_textos} ---")

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
            print(f"[INFO] Título gerado: {titulo_especifico}")

            # === GERAR ARTIGO BASEADO NO TÍTULO ===
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

            # === BUSCAR/CRIAR CATEGORIA CONFIGURADA ===
            try:
                categoria_desejada = config_execucao.get('categoria_wp', 'Others')
                categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
                categories_response = requests.get(categories_endpoint, auth=(WP_USER, WP_PASSWORD), timeout=10)
                categories_response.raise_for_status()
                
                categories = categories_response.json()
                category_id = None
                
                # Procurar categoria existente
                for cat in categories:
                    if cat['name'].lower() == categoria_desejada.lower():
                        category_id = cat['id']
                        break

                # Se não encontrou, criar nova categoria
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
                print(f"[AVISO] Erro ao buscar/criar categoria '{categoria_desejada}': {e}")
                category_id = 1  # ID padrão (Uncategorized)

            # === PUBLICAR NO WORDPRESS ===
            status_publicacao = config_execucao.get('status_publicacao', 'draft')
            post_data = {
                'title': titulo_especifico,
                'content': conteudo,
                'status': status_publicacao,
                'categories': [category_id],
                'author': config_execucao.get('author_id', 18)  # ID do autor selecionado ou padrão (mateus)
            }

            endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
            response_wp = requests.post(endpoint, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=20)
            response_wp.raise_for_status()

            status_msg = "publicado" if status_publicacao == "publish" else "salvo como rascunho"
            print(f"[✔] Post {status_msg} com sucesso na categoria '{categoria_desejada}': {titulo_especifico}")
            print(f"[INFO] Usando prompts personalizados do arquivo prompts.json")

        except Exception as e:
            print(f"[ERRO ao gerar/publicar '{titulo_especifico if 'titulo_especifico' in locals() else topico_geral}']: {e}")

        time.sleep(10)  # Evita bloqueios na API do WordPress

print("\n--- FINALIZADO COM SUCESSO ---")
print("[INFO] 🎯 Para editar os prompts, use a interface web: streamlit run app.py")
