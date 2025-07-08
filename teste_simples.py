#!/usr/bin/env python3
"""
Teste simples de credenciais WordPress
Uso: python teste_simples.py usuario senha
"""

import requests
from requests.auth import HTTPBasicAuth
import sys

def testar_wordpress(wp_url, wp_user, wp_password):
    print(f"🌐 Testando: {wp_url}")
    print(f"👤 Usuário: {wp_user}")
    
    try:
        # Teste 1: API REST
        response = requests.get(f'{wp_url}/wp-json/wp/v2', timeout=10)
        if response.status_code == 200:
            print("✅ API REST funcionando")
        else:
            print(f"⚠️ API REST: {response.status_code}")
        
        # Teste 2: Autenticação
        response = requests.get(
            f'{wp_url}/wp-json/wp/v2/users/me',
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ AUTENTICAÇÃO OK!")
            print(f"Nome: {user_data.get('name', 'N/A')}")
            print(f"ID: {user_data.get('id', 'N/A')}")
            print(f"Roles: {', '.join(user_data.get('roles', []))}")
            
            # Teste 3: Permissões para posts
            response = requests.get(
                f'{wp_url}/wp-json/wp/v2/posts',
                auth=HTTPBasicAuth(wp_user, wp_password),
                timeout=10
            )
            if response.status_code == 200:
                print("✅ Pode acessar posts")
            else:
                print(f"⚠️ Posts: {response.status_code}")
                
            return True
            
        elif response.status_code == 401:
            print("❌ AUTENTICAÇÃO FALHOU!")
            print("💡 Possíveis soluções:")
            print("   1. Verifique usuário e senha")
            print("   2. Se tem 2FA, use Application Password")
            print("   3. Verifique se usuário tem permissões API")
            return False
        else:
            print(f"⚠️ Status inesperado: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    wp_url = "https://www.elhombre.com.br"
    
    if len(sys.argv) >= 3:
        wp_user = sys.argv[1]
        wp_password = sys.argv[2]
    else:
        print("Uso: python teste_simples.py USUARIO SENHA")
        print("Exemplo: python teste_simples.py eutiago 'senha123'")
        sys.exit(1)
    
    print("🧪 TESTE DE CONEXÃO WORDPRESS")
    print("=" * 40)
    
    sucesso = testar_wordpress(wp_url, wp_user, wp_password)
    
    if sucesso:
        print("\\n🎉 CONEXÃO OK! Atualize o arquivo .env com essas credenciais.")
    else:
        print("\\n❌ CONEXÃO FALHOU! Verifique as credenciais.")
