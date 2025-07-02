import requests
from requests.auth import HTTPBasicAuth
from config import *

# Validar configurações ao iniciar
if not validar_configuracoes():
    exit(1)

url = f"{WP_URL}/wp-json/wp/v2/posts"

# Dados do post
post_data = {
    "title": "Battery technology and charging infrastructure for electric cars",
    "content": "<p>This is the body of the article. You can include <strong>HTML</strong> tags here.</p>",
    "status": "publish"  # ou "draft"
}

# Requisição com Basic Auth
response = requests.post(url, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD))

# Ver resultado
print("Status Code:", response.status_code)
print("Response:", response.text)