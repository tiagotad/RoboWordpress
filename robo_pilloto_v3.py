#!/usr/bin/env python3
"""
RoboWordpress v3 - Gerador de Conteúdo Automatizado
Sistema simplificado com prompt único
"""

import sys
import requests
import time
from datetime import datetime
from openai import OpenAI
from requests.auth import HTTPBasicAuth

# Importar configurações
from config import *
from config_execucao import get_configuracoes_execucao
from prompt_manager import get_prompt_completo, get_system_prompt

# Configurações
client = OpenAI(api_key=OPENAI_API_KEY)
config = get_configuracoes_execucao()

def log(message):
    """Log com timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def gerar_conteudo(topico):
    """Gera título e artigo usando prompt único"""
    log(f"Gerando conteúdo para: {topico}")
    
    prompt = get_prompt_completo(topico)
    system_prompt = get_system_prompt()
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    
    resposta = response.choices[0].message.content.strip()
    
    # Extrair título e artigo
    if "TÍTULO:" in resposta:
        partes = resposta.split("TÍTULO:", 1)[1].split("ARTIGO:", 1)
        titulo = partes[0].strip()
        artigo = partes[1].strip() if len(partes) > 1 else ""
    else:
        linhas = resposta.split("\n", 1)
        titulo = linhas[0].strip()
        artigo = linhas[1].strip() if len(linhas) > 1 else resposta
    
    return titulo, artigo

def publicar_post(titulo, conteudo):
    """Publica post no WordPress"""
    log(f"Publicando: {titulo}")
    
    post_data = {
        'title': titulo,
        'content': conteudo,
        'status': config.get('status_publicacao', 'draft'),
        'categories': [config.get('categoria_wp', 32174)],
        'author': config.get('author_id', 1)
    }
    
    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        json=post_data,
        auth=HTTPBasicAuth(WP_USER, WP_PASSWORD),
        timeout=20
    )
    response.raise_for_status()
    
    post_id = response.json()['id']
    log(f"✅ Post criado! ID: {post_id}")
    return post_id

def main():
    """Função principal"""
    log("🚀 Iniciando RoboWordpress v3")
    
    topicos = config.get('topicos_lista', [])
    if not topicos:
        log("❌ Nenhum tópico encontrado!")
        return
    
    log(f"📝 Processando {len(topicos)} tópicos")
    
    posts_criados = 0
    for i, topico in enumerate(topicos, 1):
        try:
            log(f"--- TÓPICO {i}/{len(topicos)}: {topico} ---")
            
            titulo, artigo = gerar_conteudo(topico)
            post_id = publicar_post(titulo, artigo)
            posts_criados += 1
            
            time.sleep(5)  # Pausa entre posts
            
        except Exception as e:
            log(f"❌ Erro no tópico '{topico}': {e}")
            continue
    
    log(f"🎉 Concluído! {posts_criados} posts criados")

if __name__ == "__main__":
    main()
