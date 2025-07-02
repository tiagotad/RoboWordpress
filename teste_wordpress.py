#!/usr/bin/env python3
# Teste simples do WordPress sem Google Sheets

import requests
import time
from openai import OpenAI
from requests.auth import HTTPBasicAuth

from config import *

# Validar configurações ao iniciar
if not validar_configuracoes():
    exit(1)

# Inicializar cliente OpenAI
client = OpenAI(api_key=OPENAI_API_KEY, timeout=30.0, max_retries=3)

# Tópicos de teste (simulando a planilha)
topicos_teste = ["Electric Vehicle Policy", "Battery Technology", "Charging Infrastructure"]

print("=== TESTE WORDPRESS - SEM GOOGLE SHEETS ===\n")

def testar_wordpress():
    """Testa conexão com WordPress"""
    try:
        print("1. Testando conexão com WordPress...")
        categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
        response = requests.get(categories_endpoint, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
        response.raise_for_status()
        print(f"✅ WordPress conectado - {len(response.json())} categorias encontradas")
        return True
    except Exception as e:
        print(f"❌ Erro no WordPress: {e}")
        return False

def testar_openai():
    """Testa conexão com OpenAI"""
    try:
        print("2. Testando conexão com OpenAI...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say 'OpenAI test successful'"}],
            max_tokens=10
        )
        print(f"✅ OpenAI conectada: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ Erro no OpenAI: {e}")
        return False

def processar_topico_teste(topico):
    """Processa um tópico de teste"""
    try:
        print(f"\n3. Processando tópico: {topico}")
        
        # Gerar título
        prompt_titulo = f"""Create ONE specific, SEO-optimized blog post title about electric cars based on "{topico}". Return ONLY the title."""
        
        response_titulo = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt_titulo}],
            max_tokens=50
        )
        
        titulo = response_titulo.choices[0].message.content.strip().strip('"')
        print(f"   ✅ Título gerado: {titulo}")
        
        # Gerar artigo curto para teste
        prompt_artigo = f'Write a 200-word blog post titled "{titulo}" about electric vehicles.'
        
        response_artigo = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt_artigo}],
            max_tokens=500
        )
        
        conteudo = response_artigo.choices[0].message.content.strip()
        print(f"   ✅ Artigo gerado ({len(conteudo)} caracteres)")
        
        # Publicar no WordPress
        post_data = {
            'title': f"[TESTE] {titulo}",
            'content': conteudo,
            'status': 'draft'
        }
        
        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        response_wp = requests.post(endpoint, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=20)
        response_wp.raise_for_status()
        
        post_id = response_wp.json()['id']
        print(f"   ✅ Rascunho criado no WordPress - ID: {post_id}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao processar tópico: {e}")
        return False

# Executar testes
if __name__ == "__main__":
    wordpress_ok = testar_wordpress()
    openai_ok = testar_openai()
    
    if wordpress_ok and openai_ok:
        print(f"\n=== PROCESSANDO {len(topicos_teste)} TÓPICOS ===")
        for i, topico in enumerate(topicos_teste, 1):
            sucesso = processar_topico_teste(topico)
            if sucesso:
                print(f"✅ Tópico {i}/{len(topicos_teste)} processado com sucesso")
            else:
                print(f"❌ Falha no tópico {i}/{len(topicos_teste)}")
            
            if i < len(topicos_teste):
                print("   Aguardando 5 segundos...")
                time.sleep(5)
        
        print("\n=== TESTE CONCLUÍDO ===")
    else:
        print("\n❌ Testes básicos falharam. Verifique as configurações.")
