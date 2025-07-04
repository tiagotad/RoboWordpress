#!/usr/bin/env python3
"""
Lista todas as categorias do WordPress para encontrar a categoria correta
"""

import requests
from requests.auth import HTTPBasicAuth
import sys

# Importar credenciais
try:
    from config import WP_URL, WP_USER, WP_PASSWORD
except ImportError:
    print("❌ Erro: Não foi possível importar credenciais do config.py")
    sys.exit(1)

def listar_todas_categorias():
    print("=== LISTAGEM DE TODAS AS CATEGORIAS ===")
    print(f"🔗 Site: {WP_URL}")
    print()
    
    try:
        # Buscar todas as categorias
        categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
        
        # Buscar com paginação para pegar todas
        all_categories = []
        page = 1
        per_page = 100
        
        while True:
            params = {
                'per_page': per_page,
                'page': page,
                'orderby': 'name',
                'order': 'asc'
            }
            
            print(f"📊 Buscando página {page}...")
            response = requests.get(categories_endpoint, params=params, 
                                  auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
            response.raise_for_status()
            
            categories = response.json()
            
            if not categories:  # Não há mais categorias
                break
                
            all_categories.extend(categories)
            
            if len(categories) < per_page:  # Última página
                break
                
            page += 1
        
        print(f"✅ Total de categorias encontradas: {len(all_categories)}")
        print()
        
        # Listar todas as categorias
        print("📁 TODAS AS CATEGORIAS:")
        print("-" * 60)
        
        for i, cat in enumerate(all_categories, 1):
            cat_id = cat.get('id')
            cat_name = cat.get('name', 'Sem nome')
            cat_slug = cat.get('slug', 'sem-slug')
            cat_count = cat.get('count', 0)
            
            print(f"{i:3d}. ID {cat_id:5d}: {cat_name}")
            print(f"     📎 Slug: {cat_slug}")
            print(f"     📊 Posts: {cat_count}")
            print()
        
        # Procurar especificamente por "mundo"
        print("🔍 PROCURANDO CATEGORIA 'MUNDO':")
        print("-" * 40)
        
        categorias_mundo = []
        for cat in all_categories:
            cat_name = cat.get('name', '').lower()
            if 'mundo' in cat_name:
                categorias_mundo.append(cat)
        
        if categorias_mundo:
            print(f"✅ Encontradas {len(categorias_mundo)} categorias relacionadas a 'mundo':")
            for cat in categorias_mundo:
                print(f"   🎯 ID {cat['id']}: {cat['name']} (slug: {cat['slug']}, posts: {cat['count']})")
        else:
            print("❌ Nenhuma categoria com 'mundo' no nome encontrada")
        
        print()
        
        # Procurar por categorias com mais posts (principais)
        print("📊 TOP 10 CATEGORIAS COM MAIS POSTS:")
        print("-" * 45)
        
        top_categories = sorted(all_categories, key=lambda x: x.get('count', 0), reverse=True)[:10]
        
        for i, cat in enumerate(top_categories, 1):
            print(f"{i:2d}. ID {cat['id']:5d}: {cat['name']} ({cat['count']} posts)")
        
        print()
        
        # Verificar se ID 32174 existe mesmo
        categoria_32174 = next((cat for cat in all_categories if cat['id'] == 32174), None)
        if categoria_32174:
            print(f"✅ ID 32174 encontrado: {categoria_32174['name']}")
        else:
            print("❌ Confirmado: ID 32174 NÃO existe")
            
            # Sugerir uma categoria principal
            if top_categories:
                main_cat = top_categories[0]
                print(f"💡 Sugestão: Usar categoria principal ID {main_cat['id']}: '{main_cat['name']}' ({main_cat['count']} posts)")
                
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    listar_todas_categorias()
