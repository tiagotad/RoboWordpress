#!/usr/bin/env python3
"""
Busca rápida pela categoria 'mundo' ou similares
"""

import requests
from requests.auth import HTTPBasicAuth
import sys

try:
    from config import WP_URL, WP_USER, WP_PASSWORD
except ImportError:
    print("❌ Erro: credenciais")
    sys.exit(1)

def buscar_categoria_mundo():
    print("🔍 Buscando categoria 'mundo'...")
    
    try:
        # Buscar categorias
        url = f"{WP_URL}/wp-json/wp/v2/categories"
        params = {'per_page': 100, 'search': 'mundo'}
        
        response = requests.get(url, params=params, 
                              auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
        response.raise_for_status()
        
        categories = response.json()
        
        print(f"✅ Encontradas {len(categories)} categorias com 'mundo'")
        
        for cat in categories:
            print(f"ID {cat['id']}: {cat['name']} (slug: {cat['slug']}, posts: {cat['count']})")
        
        if not categories:
            print("❌ Nenhuma categoria 'mundo' encontrada")
            
            # Buscar as principais
            print("\n🔍 Top 5 categorias principais:")
            response2 = requests.get(url, params={'per_page': 5, 'orderby': 'count', 'order': 'desc'}, 
                                   auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
            top_cats = response2.json()
            
            for cat in top_cats:
                print(f"ID {cat['id']}: {cat['name']} ({cat['count']} posts)")
                
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    buscar_categoria_mundo()
