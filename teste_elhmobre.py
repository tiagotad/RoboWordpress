#!/usr/bin/env python3
"""
Script para testar conexão com o novo site WordPress elhmobre.com
"""

import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json

def log_with_timestamp(message):
    """Adiciona timestamp aos logs"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def testar_wordpress(wp_url, wp_user, wp_password):
    """Testa conexão com WordPress"""
    
    log_with_timestamp(f"🌐 Testando conexão com: {wp_url}")
    log_with_timestamp(f"👤 Usuário: {wp_user}")
    
    try:
        # Teste 1: Verificar se a API REST está disponível
        log_with_timestamp("1️⃣ Verificando se API REST está ativa...")
        
        api_endpoint = f"{wp_url}/wp-json/wp/v2"
        response = requests.get(api_endpoint, timeout=10)
        
        if response.status_code == 200:
            log_with_timestamp("✅ API REST está funcionando!")
        else:
            log_with_timestamp(f"⚠️ API REST retornou código: {response.status_code}")
            
        # Teste 2: Verificar autenticação
        log_with_timestamp("2️⃣ Testando autenticação...")
        
        auth_endpoint = f"{wp_url}/wp-json/wp/v2/users/me"
        response = requests.get(
            auth_endpoint,
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            log_with_timestamp(f"✅ Autenticação OK! Usuário: {user_data.get('name', 'N/A')}")
            log_with_timestamp(f"📋 ID: {user_data.get('id', 'N/A')}")
            log_with_timestamp(f"📧 Email: {user_data.get('email', 'N/A')}")
            log_with_timestamp(f"🔑 Roles: {', '.join(user_data.get('roles', []))}")
            
        elif response.status_code == 401:
            log_with_timestamp("❌ Falha na autenticação! Verifique usuário e senha.")
            log_with_timestamp("💡 Dica: Use Application Password se tiver 2FA ativado")
            return False
            
        elif response.status_code == 403:
            log_with_timestamp("❌ Acesso negado! Usuário não tem permissões suficientes.")
            return False
            
        else:
            log_with_timestamp(f"⚠️ Resposta inesperada: {response.status_code}")
            log_with_timestamp(f"Detalhes: {response.text[:200]}")
            
        # Teste 3: Verificar permissões para criar posts
        log_with_timestamp("3️⃣ Verificando permissões para criar posts...")
        
        posts_endpoint = f"{wp_url}/wp-json/wp/v2/posts"
        response = requests.options(
            posts_endpoint,
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        if response.status_code in [200, 204]:
            allow_header = response.headers.get('Allow', '')
            if 'POST' in allow_header:
                log_with_timestamp("✅ Permissão para criar posts: OK!")
            else:
                log_with_timestamp("⚠️ Pode não ter permissão para criar posts")
        else:
            log_with_timestamp(f"⚠️ Não foi possível verificar permissões: {response.status_code}")
            
        # Teste 4: Listar categorias
        log_with_timestamp("4️⃣ Listando categorias disponíveis...")
        
        categories_endpoint = f"{wp_url}/wp-json/wp/v2/categories"
        response = requests.get(
            categories_endpoint,
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        if response.status_code == 200:
            categories = response.json()
            log_with_timestamp(f"✅ {len(categories)} categorias encontradas:")
            for cat in categories[:5]:  # Mostrar apenas as primeiras 5
                log_with_timestamp(f"   📁 {cat['name']} (ID: {cat['id']})")
        else:
            log_with_timestamp(f"⚠️ Não foi possível listar categorias: {response.status_code}")
            
        log_with_timestamp("🎉 Teste concluído!")
        return True
        
    except requests.exceptions.ConnectionError:
        log_with_timestamp("❌ Erro de conexão! Verifique se o site está online.")
        return False
    except requests.exceptions.Timeout:
        log_with_timestamp("❌ Timeout! O site demorou muito para responder.")
        return False
    except Exception as e:
        log_with_timestamp(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    # Tentar carregar do arquivo .env primeiro
    try:
        from config import WP_URL, WP_USER, WP_PASSWORD
        log_with_timestamp(f"✅ Credenciais carregadas do .env:")
        log_with_timestamp(f"   URL: {WP_URL}")
        log_with_timestamp(f"   Usuário: {WP_USER}")
    except Exception as e:
        log_with_timestamp(f"⚠️ Erro ao carregar .env: {e}")
        # Configurações para teste manual
        WP_URL = "https://elhombre.com.com.br"
        WP_USER = "eutiago"
        WP_PASSWORD = "Franz@Monet2017!@#"
    
    print("=" * 60)
    print("🧪 TESTE DE CONEXÃO WORDPRESS - ELHOMBRE.COM.BR")
    print("=" * 60)
    
    # Solicitar credenciais se não estiverem definidas
    if not WP_PASSWORD or WP_PASSWORD == "COLOQUE_SUA_SENHA_AQUI":
        print("⚠️ CONFIGURE AS CREDENCIAIS PRIMEIRO!")
        print("Edite o arquivo .env e coloque suas credenciais reais")
        exit(1)
    
    # Executar teste
    sucesso = testar_wordpress(WP_URL, WP_USER, WP_PASSWORD)
    
    if sucesso:
        print("\n✅ CONEXÃO OK! Você pode usar estas credenciais no RoboWordpress.")
    else:
        print("\n❌ CONEXÃO FALHOU! Verifique as credenciais e tente novamente.")
