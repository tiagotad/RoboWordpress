import requests
from requests.auth import HTTPBasicAuth

def buscar_autores_wordpress(wp_url, wp_user, wp_password):
    """Busca a lista de autores do WordPress via API REST"""
    try:
        endpoint = f"{wp_url}/wp-json/wp/v2/users"
        response = requests.get(endpoint, auth=HTTPBasicAuth(wp_user, wp_password), timeout=10)
        response.raise_for_status()
        users = response.json()
        autores = [(user['id'], user['name']) for user in users]
        return autores
    except Exception as e:
        return []
