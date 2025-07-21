#!/usr/bin/env python3
"""
Teste simples para validar credenciais WordPress
"""

import requests
from requests.auth import HTTPBasicAuth

def testar_credenciais(wp_url, wp_user, wp_password):
    """Testa as credenciais do WordPress"""
    print(f"🔍 TESTANDO CREDENCIAIS PARA {wp_url}")
    print(f"👤 Usuário: {wp_user}")
    print(f"🔑 Senha: {'*' * len(wp_password)}")
    print("-" * 50)
    
    try:
        # Teste básico de conectividade
        print("1. Testando conectividade com o site...")
        response = requests.get(wp_url, timeout=10)
        print(f"   ✅ Site acessível - Status: {response.status_code}")
        
        # Teste da API REST
        print("2. Testando API REST...")
        api_url = f"{wp_url}/wp-json/wp/v2/"
        api_response = requests.get(api_url, timeout=10)
        print(f"   ✅ API REST ativa - Status: {api_response.status_code}")
        
        # Teste de autenticação
        print("3. Testando autenticação...")
        auth_url = f"{wp_url}/wp-json/wp/v2/users/me"
        auth_response = requests.get(
            auth_url,
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        if auth_response.status_code == 200:
            user_data = auth_response.json()
            print(f"   ✅ AUTENTICAÇÃO VÁLIDA!")
            print(f"   👤 Logado como: {user_data.get('name', 'N/A')}")
            print(f"   🆔 ID do usuário: {user_data.get('id', 'N/A')}")
            print(f"   📧 Email: {user_data.get('email', 'N/A')}")
            return True
        elif auth_response.status_code == 401:
            print(f"   ❌ FALHA NA AUTENTICAÇÃO!")
            print(f"   ⚠️  Usuário ou senha incorretos")
            return False
        else:
            print(f"   ❌ ERRO: Status {auth_response.status_code}")
            print(f"   📝 Resposta: {auth_response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ ERRO: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔑 TESTE DE CREDENCIAIS WORDPRESS")
    print("=" * 60)
    
    # Configurações atuais (EDITE AQUI)
    wp_url = "https://thenextavenue.com"
    wp_user = input("Digite o usuário WordPress: ")
    wp_password = input("Digite a senha/app password: ")
    
    if wp_user and wp_password:
        sucesso = testar_credenciais(wp_url, wp_user, wp_password)
        
        if sucesso:
            print("\n🎉 CREDENCIAIS VÁLIDAS!")
            print("Agora você pode atualizar o arquivo config_execucao.py")
        else:
            print("\n❌ CREDENCIAIS INVÁLIDAS!")
            print("Verifique o usuário e senha e tente novamente")
    else:
        print("❌ Usuário e senha são obrigatórios!")
