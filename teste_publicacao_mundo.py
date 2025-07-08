#!/usr/bin/env python3
"""
Teste simples para verificar se a publicação na categoria mundo (32174) funciona
"""

import requests
from requests.auth import HTTPBasicAuth
import sys
from datetime import datetime

try:
    from config import WP_URL, WP_USER, WP_PASSWORD
    from config_execucao import get_configuracoes_execucao
except ImportError:
    print("❌ Erro: Não foi possível importar configurações")
    sys.exit(1)

def testar_publicacao_categoria():
    print("=== TESTE DE PUBLICAÇÃO NA CATEGORIA MUNDO ===")
    print(f"🔗 Site: {WP_URL}")
    print(f"👤 Usuário: {WP_USER}")
    print()
    
    # Verificar configuração atual
    config = get_configuracoes_execucao()
    categoria_config = config.get('categoria_wp', 'Não definida')
    print(f"📁 Categoria configurada: {categoria_config} (tipo: {type(categoria_config).__name__})")
    
    if categoria_config != 32174:
        print(f"⚠️ ATENÇÃO: Categoria não é 32174! Valor atual: {categoria_config}")
        return False
    
    # Verificar se categoria 32174 existe
    print("\n🔍 Verificando se categoria 32174 existe...")
    try:
        category_check_url = f"{WP_URL}/wp-json/wp/v2/categories/32174"
        response = requests.get(category_check_url, 
                              auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
        
        if response.status_code == 200:
            categoria_info = response.json()
            print(f"✅ Categoria 32174 existe: '{categoria_info['name']}'")
            print(f"   📊 Posts atuais na categoria: {categoria_info['count']}")
        else:
            print(f"❌ Categoria 32174 não encontrada (status: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar categoria: {e}")
        return False
    
    # Criar post de teste na categoria
    print("\n📝 Criando post de teste na categoria mundo...")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    post_data = {
        'title': f'TESTE - Post na categoria mundo - {timestamp}',
        'content': f'<p>Este é um teste para verificar se o post é criado na categoria "mundo" (ID 32174).</p><p>Criado em: {timestamp}</p>',
        'status': 'draft',  # Criar como rascunho
        'categories': [32174],  # Categoria mundo
        'author': config.get('author_id', 1)
    }
    
    try:
        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        response = requests.post(endpoint, json=post_data, 
                               auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=20)
        response.raise_for_status()
        
        post_response = response.json()
        post_id = post_response['id']
        post_categories = post_response.get('categories', [])
        
        print(f"✅ Post criado com sucesso!")
        print(f"   🆔 ID do post: {post_id}")
        print(f"   📁 Categorias: {post_categories}")
        
        if 32174 in post_categories:
            print("🎉 SUCESSO: Post foi criado na categoria mundo (32174)!")
        else:
            print(f"❌ FALHA: Post não foi criado na categoria mundo. Categorias: {post_categories}")
            
        print(f"   🔗 URL: {WP_URL}/?p={post_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar post: {e}")
        return False

if __name__ == "__main__":
    testar_publicacao_categoria()
