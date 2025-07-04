"""
Utilitários para o aplicativo RoboWordpress
"""
import requests
from requests.auth import HTTPBasicAuth

def buscar_autores_wordpress(wp_url, wp_user, wp_password):
    """
    Busca lista de autores do WordPress via API REST
    
    Args:
        wp_url (str): URL do site WordPress
        wp_user (str): Usuário do WordPress
        wp_password (str): Senha/Application Password do WordPress
    
    Returns:
        list: Lista de tuplas (id, nome) dos autores
    """
    try:
        # URL da API para buscar usuários/autores
        api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/users"
        
        # Fazer requisição com autenticação
        response = requests.get(
            api_url,
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        if response.status_code == 200:
            usuarios = response.json()
            # Retornar lista de (id, nome) dos autores
            autores = [(user['id'], user['name']) for user in usuarios]
            return autores
        else:
            print(f"[ERRO] Falha ao buscar autores: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"[ERRO] Erro ao conectar com WordPress: {e}")
        return []

def validar_conexao_wordpress(wp_url, wp_user, wp_password):
    """
    Valida se a conexão com WordPress está funcionando
    
    Args:
        wp_url (str): URL do site WordPress
        wp_user (str): Usuário do WordPress
        wp_password (str): Senha/Application Password do WordPress
    
    Returns:
        bool: True se conexão OK, False caso contrário
    """
    try:
        # Testar conexão básica com a API
        api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
        
        response = requests.get(
            api_url,
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10,
            params={'per_page': 1}  # Buscar apenas 1 post para teste
        )
        
        return response.status_code in [200, 401]  # 401 também indica que a API está acessível
        
    except Exception as e:
        print(f"[ERRO] Erro na validação: {e}")
        return False
