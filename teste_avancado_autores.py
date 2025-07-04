#!/usr/bin/env python3
"""
Teste avançado para carregar todos os autores do WordPress
"""

import os
import sys
import requests
from requests.auth import HTTPBasicAuth

# Adicionar diretório atual ao path
sys.path.append(os.getcwd())

def teste_avancado_autores():
    # Credenciais
    wp_url = "https://www.elhombre.com.br"
    wp_user = "eutiago"
    wp_password = "oJrD 8N3S 7SPp 0Zcz q1vz o0Gd"
    
    print("🔍 TESTE AVANÇADO DE CARREGAMENTO DE AUTORES")
    print("=" * 60)
    print(f"Site: {wp_url}")
    print(f"Usuário: {wp_user}")
    print()
    
    # Teste 1: Verificar endpoints disponíveis
    print("📊 Teste 1: Verificando endpoints da API...")
    try:
        response = requests.get(f"{wp_url}/wp-json/wp/v2", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'routes' in data:
                user_routes = [route for route in data['routes'].keys() if 'user' in route.lower()]
                print(f"✅ Endpoints relacionados a usuários encontrados: {user_routes}")
            else:
                print("✅ API funcionando, mas sem informações de rotas")
        else:
            print(f"⚠️ API respondeu com status {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao acessar API: {e}")
    
    print()
    
    # Teste 2: Tentar diferentes contextos e parâmetros
    print("🔧 Teste 2: Tentando diferentes parâmetros...")
    
    test_params = [
        {},
        {'context': 'edit'},
        {'context': 'view'},
        {'per_page': 100},
        {'per_page': 50},
        {'per_page': 10},
        {'context': 'view', 'per_page': 100},
        {'context': 'edit', 'per_page': 100},
        {'orderby': 'name', 'order': 'asc'},
    ]
    
    api_url = f"{wp_url}/wp-json/wp/v2/users"
    
    for i, params in enumerate(test_params):
        print(f"  Tentativa {i+1}: {params if params else 'sem parâmetros'}")
        try:
            response = requests.get(
                api_url,
                auth=HTTPBasicAuth(wp_user, wp_password),
                timeout=10,
                params=params
            )
            
            if response.status_code == 200:
                users = response.json()
                print(f"    ✅ Sucesso! {len(users)} usuários encontrados")
                if users:
                    # Verificar se ID 210 está na lista
                    user_210 = next((user for user in users if user.get('id') == 210), None)
                    if user_210:
                        print(f"    🎯 ID 210 encontrado: {user_210.get('name', 'N/A')}")
                    else:
                        print(f"    ⚠️ ID 210 não encontrado na lista")
                    
                    # Mostrar alguns usuários
                    print(f"    👥 Primeiros usuários:")
                    for user in users[:5]:
                        print(f"      - ID: {user.get('id')} | Nome: {user.get('name', 'N/A')}")
                    if len(users) > 5:
                        print(f"      ... e mais {len(users) - 5} usuários")
                break  # Parar no primeiro sucesso
            else:
                print(f"    ❌ Falha: {response.status_code}")
                if response.status_code == 401:
                    print(f"      → Credenciais inválidas ou sem permissão")
                elif response.status_code == 403:
                    print(f"      → Acesso negado (permissões insuficientes)")
                    
        except Exception as e:
            print(f"    ❌ Erro: {e}")
    
    print()
    
    # Teste 3: Verificar usuário atual
    print("👤 Teste 3: Verificando usuário atual...")
    try:
        response = requests.get(
            f"{wp_url}/wp-json/wp/v2/users/me",
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Usuário atual: ID {user_data.get('id')} - {user_data.get('name', 'N/A')}")
            print(f"   Roles: {user_data.get('roles', [])}")
            print(f"   Capabilities: {len(user_data.get('capabilities', {}))} permissões")
        else:
            print(f"❌ Falha ao buscar usuário atual: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao buscar usuário atual: {e}")
    
    print()
    
    # Teste 4: Buscar usuário específico (ID 210)
    print("🎯 Teste 4: Tentando buscar usuário ID 210 diretamente...")
    try:
        response = requests.get(
            f"{wp_url}/wp-json/wp/v2/users/210",
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Usuário ID 210 encontrado: {user_data.get('name', 'N/A')}")
            print(f"   Slug: {user_data.get('slug', 'N/A')}")
            print(f"   Email: {user_data.get('email', 'N/A')}")
        elif response.status_code == 404:
            print(f"❌ Usuário ID 210 não existe no WordPress")
        else:
            print(f"❌ Erro ao buscar usuário ID 210: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro ao buscar usuário ID 210: {e}")

if __name__ == "__main__":
    teste_avancado_autores()
