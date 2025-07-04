#!/usr/bin/env python3
"""
Script para testar rapidamente se o robô está funcionando
sem executar um post completo - apenas testa a geração de título
"""

import sys
import os
from datetime import datetime

def log_with_timestamp(message):
    """Adiciona timestamp aos logs"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

try:
    # Importar configurações
    from config import WP_URL, WP_USER, WP_PASSWORD, OPENAI_API_KEY
    from openai import OpenAI
    
    log_with_timestamp("🔧 Testando configurações...")
    
    # Testar cliente OpenAI
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        timeout=30.0,
        max_retries=1
    )
    
    log_with_timestamp("🤖 Testando geração de título rápido...")
    
    # Teste simples de geração
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um gerador de títulos de blog. Seja criativo e direto."},
            {"role": "user", "content": "Crie um título interessante sobre 'Tecnologia'"}
        ],
        temperature=0.8,
        max_tokens=50,
        timeout=15
    )
    
    titulo = response.choices[0].message.content.strip()
    log_with_timestamp(f"✅ Título gerado com sucesso: {titulo}")
    
    log_with_timestamp("🌐 Testando conexão WordPress...")
    
    # Testar conexão WordPress
    import requests
    from requests.auth import HTTPBasicAuth
    
    # Apenas testar se consegue acessar a API
    endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
    headers = {'User-Agent': 'RoboWordpress-Test/1.0'}
    
    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/users/me",
        auth=HTTPBasicAuth(WP_USER, WP_PASSWORD),
        timeout=10,
        headers=headers
    )
    
    if response.status_code == 200:
        user_data = response.json()
        log_with_timestamp(f"✅ WordPress conectado com sucesso! Usuário: {user_data.get('name', WP_USER)}")
    else:
        log_with_timestamp(f"⚠️ WordPress respondeu com código: {response.status_code}")
        
    log_with_timestamp("🎉 Teste concluído! O robô deve funcionar normalmente.")
    
except Exception as e:
    log_with_timestamp(f"❌ Erro durante o teste: {e}")
    log_with_timestamp(f"Tipo do erro: {type(e).__name__}")
    sys.exit(1)
