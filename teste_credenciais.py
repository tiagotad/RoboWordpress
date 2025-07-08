#!/usr/bin/env python3
"""
Script interativo para testar credenciais do WordPress
"""

import requests
from requests.auth import HTTPBasicAuth
import getpass

def testar_credenciais(wp_url, wp_user, wp_password):
    """Testa credenciais do WordPress"""
    
    print(f"🌐 Testando: {wp_url}")
    print(f"👤 Usuário: {wp_user}")
    print(f"🔐 Senha: {'*' * len(wp_password)}")
    
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
            print(f"✅ AUTENTICAÇÃO OK!")
            print(f"📝 Nome: {user_data.get('name', 'N/A')}")
            print(f"🆔 ID: {user_data.get('id', 'N/A')}")
            print(f"📧 Email: {user_data.get('email', 'N/A')}")
            print(f"🔑 Roles: {', '.join(user_data.get('roles', []))}")
            return True
            
        elif response.status_code == 401:
            print(f"❌ FALHA NA AUTENTICAÇÃO")
            print(f"Mensagem: {response.json().get('message', 'N/A')}")
            return False
            
        else:
            print(f"⚠️ STATUS INESPERADO: {response.status_code}")
            print(f"Resposta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ ERRO DE CONEXÃO: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 TESTE DE CREDENCIAIS WORDPRESS - ELHOMBRE.COM.BR")
    print("=" * 60)
    
    wp_url = "https://www.elhombre.com.br"
    
    print("\\n💡 DICAS IMPORTANTES:")
    print("- Se tiver 2FA ativo, use Application Password")
    print("- Application Password: WordPress Admin → Usuários → Seu Perfil → Application Passwords")
    print("- Format: username:application_password")
    print("")
    
    while True:
        print("\\n📝 Digite suas credenciais:")
        wp_user = input("Usuário: ").strip()
        wp_password = getpass.getpass("Senha: ").strip()
        
        if not wp_user or not wp_password:
            print("❌ Usuário e senha são obrigatórios!")
            continue
            
        print("\\n🔍 Testando credenciais...")
        sucesso = testar_credenciais(wp_url, wp_user, wp_password)
        
        if sucesso:
            print("\\n🎉 CREDENCIAIS VÁLIDAS!")
            print("\\n📋 Para usar no RoboWordpress, edite o arquivo .env:")
            print(f"WP_URL={wp_url}")
            print(f"WP_USER={wp_user}")
            print(f"WP_PASSWORD={wp_password}")
            break
        else:
            print("\\n❌ Credenciais inválidas. Tente novamente.")
            continuar = input("\\nTentar novamente? (s/n): ").lower()
            if continuar != 's':
                break

if __name__ == "__main__":
    main()
