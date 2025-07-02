#!/usr/bin/env python3
# Robô Piloto - Versão Simplificada (sem Google Sheets)


import sys
import os
import requests
import time
from openai import OpenAI
from requests.auth import HTTPBasicAuth

# Importação condicional de configuração (local ou cloud)
try:
    import streamlit as st
    if hasattr(st, "secrets") and "WP_URL" in st.secrets:
        from config_cloud import *
    else:
        from config import *
except ImportError:
    from config import *

# Validar configurações ao iniciar
if not validar_configuracoes():
    exit(1)

# Inicializar cliente OpenAI
client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=30.0,
    max_retries=3
)

# Tópicos de entretenimento
topicos = [
    "Filmes e Cinema",
    "Séries de TV", 
    "História e Curiosidades"
]

print("=== ROBÔ PILOTO - ENTRETENIMENTO ===")
print(f"Processando {len(topicos)} tópicos para o site: {WP_URL}")

for i, topico_geral in enumerate(topicos, 1):
    print(f"\n[{i}/{len(topicos)}] PROCESSANDO: {topico_geral}")

    try:
        # === GERAR TÍTULO ===
        prompt_titulo = f"""
Você é um especialista em criação de conteúdo para entretenimento. Com base no tópico "{topico_geral}", crie UM título específico e otimizado para SEO em Português.

O título deve:
• Focar em tendências recentes ou eventos atuais
• Ser altamente pesquisável
• Ter entre 50-80 caracteres
• Incluir palavras-chave populares

Retorne APENAS o título.
"""

        response_titulo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um jornalista especializado em entretenimento e SEO."},
                {"role": "user", "content": prompt_titulo}
            ],
            temperature=0.8,
            max_tokens=120
        )

        titulo_especifico = response_titulo.choices[0].message.content.strip().strip('"')
        print(f"   ✅ Título: {titulo_especifico}")

        # === GERAR ARTIGO ===
        prompt_artigo = f"""
Escreva um artigo completo de 1000-1200 palavras com o título: "{titulo_especifico}"

ESTRUTURA OBRIGATÓRIA:
1. Introdução atrativa (150-200 palavras)
2. 3-4 seções principais com subtítulos H2
3. Listas com marcadores quando relevante
4. Conclusão envolvente (100-150 palavras)

REQUISITOS SEO:
• Use palavras-chave naturalmente
• Inclua subtítulos otimizados
• Adicione dados específicos e estatísticas
• Tom conversacional e informativo

Foco: {topico_geral}
"""

        response_artigo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um jornalista especializado em entretenimento que cria conteúdo SEO otimizado."},
                {"role": "user", "content": prompt_artigo}
            ],
            temperature=0.7,
            max_tokens=3000
        )

        conteudo = response_artigo.choices[0].message.content.strip()
        print(f"   ✅ Artigo gerado ({len(conteudo)} caracteres)")

        # === BUSCAR/CRIAR CATEGORIA "Others" ===
        try:
            categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
            categories_response = requests.get(categories_endpoint, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
            categories_response.raise_for_status()
            
            categories = categories_response.json()
            others_category_id = None
            
            for category in categories:
                if category['name'].lower() == 'others':
                    others_category_id = category['id']
                    break
            
            if others_category_id is None:
                create_category_data = {'name': 'Others', 'slug': 'others'}
                create_response = requests.post(categories_endpoint, json=create_category_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
                create_response.raise_for_status()
                others_category_id = create_response.json()['id']
                print(f"   ✅ Categoria 'Others' criada (ID: {others_category_id})")
            
        except Exception as e:
            print(f"   ⚠️  Erro na categoria: {e}")
            others_category_id = 1

        # === PUBLICAR NO WORDPRESS ===
        post_data = {
            'title': titulo_especifico,
            'content': conteudo,
            'status': 'draft',
            'categories': [others_category_id]
        }

        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        response_wp = requests.post(endpoint, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=20)
        response_wp.raise_for_status()

        post_id = response_wp.json()['id']
        print(f"   ✅ RASCUNHO CRIADO - ID: {post_id}")
        print(f"   📝 Título: {titulo_especifico}")

    except Exception as e:
        print(f"   ❌ ERRO: {e}")

    # Pausa entre posts
    if i < len(topicos):
        print("   ⏱️  Aguardando 10 segundos...")
        time.sleep(10)

print(f"\n🎉 PROCESSO CONCLUÍDO!")
print(f"✅ {len(topicos)} tópicos processados")
print(f"🌐 Verifique os rascunhos em: {WP_URL}/wp-admin")
