#!/usr/bin/env python3
# Teste de conexão WordPress

from config import *
import requests

def test_wordpress():
    try:
        # Testar categorias
        print("🔗 Testando conexão com WordPress...")
        url = f'{WP_URL}/wp-json/wp/v2/categories'
        response = requests.get(url, auth=(WP_USER, WP_PASSWORD), timeout=10)
        print(f'Status da API de categorias: {response.status_code}')
        
        if response.status_code == 200:
            categories = response.json()
            print(f'✅ {len(categories)} categorias encontradas:')
            for cat in categories[:5]:
                print(f'  - {cat["name"]} (ID: {cat["id"]})')
        else:
            print(f'❌ Erro ao buscar categorias: {response.text}')
        
        # Testar usuários/autores
        print("\n👤 Testando busca de autores...")
        url = f'{WP_URL}/wp-json/wp/v2/users'
        response = requests.get(url, auth=(WP_USER, WP_PASSWORD), timeout=10)
        print(f'Status da API de usuários: {response.status_code}')
        
        if response.status_code == 200:
            users = response.json()
            print(f'✅ {len(users)} usuários encontrados:')
            for user in users:
                print(f'  - {user["name"]} (ID: {user["id"]}, Slug: {user["slug"]})')
        else:
            print(f'❌ Erro ao buscar usuários: {response.text}')
            
    except Exception as e:
        print(f'❌ Erro de conexão: {e}')

if __name__ == "__main__":
    test_wordpress()
