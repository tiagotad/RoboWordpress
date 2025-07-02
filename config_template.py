import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do WordPress
WP_URL = os.getenv('WP_URL', 'https://exemplo.com')
WP_USER = os.getenv('WP_USER', 'usuario')
WP_PASSWORD = os.getenv('WP_PASSWORD', 'senha')

# Configurações da OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Configurações do Google Sheets
GOOGLE_SHEET_NAME = os.getenv('GOOGLE_SHEET_NAME', 'TopicosBlog')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID', '')
CREDENTIALS_JSON = os.getenv('CREDENTIALS_JSON', 'credenciais_google.json')
CREDENTIALS_FILE = CREDENTIALS_JSON  # Alias para compatibilidade

# Validação das configurações obrigatórias
def validar_configuracoes():
    """Valida se todas as configurações necessárias estão definidas"""
    erros = []
    
    if not OPENAI_API_KEY:
        erros.append("OPENAI_API_KEY não está definida")
    
    if not WP_PASSWORD or WP_PASSWORD == 'senha':
        erros.append("WP_PASSWORD não está definida corretamente")
    
    if erros:
        print("❌ Configurações faltando:")
        for erro in erros:
            print(f"  - {erro}")
        print("\n💡 Crie um arquivo .env baseado no .env.example")
        return False
    
    return True
