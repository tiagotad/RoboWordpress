#!/usr/bin/env python3
"""
Teste para verificar em qual categoria os posts estão sendo publicados
"""

import requests
from requests.auth import HTTPBasicAuth
import sys
import os
from datetime import datetime, timedelta

# Importar credenciais
try:
    from config import WP_URL, WP_USER, WP_PASSWORD
except ImportError:
    print("❌ Erro: Não foi possível importar credenciais do config.py")
    sys.exit(1)

def verificar_posts_recentes():
    print("=== TESTE DE CATEGORIA DE PUBLICAÇÃO ===")
    print(f"🔗 Site: {WP_URL}")
    print(f"👤 Usuário: {WP_USER}")
    print()
    
    try:
        # Buscar posts dos últimos 2 dias
        posts_endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        
        # Data de 2 dias atrás
        dois_dias_atras = (datetime.now() - timedelta(days=2)).isoformat()
        
        params = {
            'per_page': 10,
            'orderby': 'date',
            'order': 'desc',
            'after': dois_dias_atras
        }
        
        print("📊 Buscando posts recentes...")
        response = requests.get(posts_endpoint, params=params, 
                              auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
        response.raise_for_status()
        
        posts = response.json()
        print(f"✅ Encontrados {len(posts)} posts recentes")
        print()
        
        if not posts:
            print("ℹ️ Nenhum post encontrado nos últimos 2 dias")
            return
        
        # Buscar todas as categorias para mapear IDs para nomes
        print("📁 Buscando categorias...")
        categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
        cat_response = requests.get(categories_endpoint, 
                                  auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
        cat_response.raise_for_status()
        
        categories = cat_response.json()
        category_map = {cat['id']: cat['name'] for cat in categories}
        
        print("✅ Categorias carregadas")
        print()
        
        # Analisar cada post
        print("📝 POSTS RECENTES E SUAS CATEGORIAS:")
        print("-" * 80)
        
        for i, post in enumerate(posts, 1):
            titulo = post.get('title', {}).get('rendered', 'Sem título')
            post_id = post.get('id')
            date = post.get('date', '')
            categories_ids = post.get('categories', [])
            author_id = post.get('author', 'N/A')
            
            print(f"{i}. 📄 {titulo}")
            print(f"   🆔 ID: {post_id}")
            print(f"   📅 Data: {date}")
            print(f"   👤 Autor ID: {author_id}")
            
            if categories_ids:
                print("   📁 Categorias:")
                for cat_id in categories_ids:
                    cat_name = category_map.get(cat_id, f"ID {cat_id} (nome não encontrado)")
                    print(f"      - ID {cat_id}: {cat_name}")
                    
                    if cat_id == 32174:
                        print("      ✅ ESTÁ na categoria 'mundo' (ID 32174)!")
                    elif cat_id != 32174:
                        print(f"      ⚠️ NÃO está na categoria 'mundo' (está em ID {cat_id})")
            else:
                print("   📁 Sem categoria definida")
            
            print()
        
        # Verificar especificamente a categoria 32174
        print("🔍 VERIFICAÇÃO ESPECÍFICA DA CATEGORIA 'MUNDO' (ID 32174):")
        print("-" * 60)
        
        categoria_32174 = category_map.get(32174)
        if categoria_32174:
            print(f"✅ Categoria ID 32174 existe: '{categoria_32174}'")
            
            # Contar posts nesta categoria
            posts_na_categoria = sum(1 for post in posts if 32174 in post.get('categories', []))
            print(f"📊 Posts recentes na categoria 'mundo': {posts_na_categoria}/{len(posts)}")
            
        else:
            print("❌ Categoria ID 32174 não encontrada!")
            
            # Buscar categoria 'mundo' por nome
            categoria_mundo = None
            for cat_id, cat_name in category_map.items():
                if cat_name.lower() == 'mundo':
                    categoria_mundo = (cat_id, cat_name)
                    break
            
            if categoria_mundo:
                print(f"🔍 Encontrada categoria 'mundo' com ID diferente: {categoria_mundo[0]} - '{categoria_mundo[1]}'")
            else:
                print("❌ Categoria 'mundo' não encontrada por nome também!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    verificar_posts_recentes()
