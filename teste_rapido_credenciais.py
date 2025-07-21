#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth

wp_url = "https://thenextavenue.com"
wp_user = "tiagotad"
wp_password = "hd5G t0dB wSCu f9pS IQjV bm8W"

print("🔍 TESTANDO CONEXÃO WordPress")
print(f"🌐 Site: {wp_url}")
print(f"👤 Usuário: {wp_user}")
print(f"🔑 Senha: {'*' * len(wp_password)}")
print("-" * 50)

try:
    # Teste de autenticação
    response = requests.get(
        f'{wp_url}/wp-json/wp/v2/users/me',
        auth=HTTPBasicAuth(wp_user, wp_password),
        timeout=10
    )
    
    print(f"📡 Status: {response.status_code}")
    
    if response.status_code == 200:
        user_data = response.json()
        print("✅ AUTENTICAÇÃO VÁLIDA!")
        print(f"👤 Nome: {user_data.get('name', 'N/A')}")
        print(f"🆔 ID: {user_data.get('id', 'N/A')}")
        print(f"📧 Email: {user_data.get('email', 'N/A')}")
    elif response.status_code == 401:
        print("❌ FALHA NA AUTENTICAÇÃO!")
        print("⚠️ Usuário ou senha incorretos")
    else:
        print(f"❌ ERRO: Status {response.status_code}")
        
except Exception as e:
    print(f"❌ ERRO: {str(e)}")
