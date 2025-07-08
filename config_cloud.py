import os

def _get_secret(key, default=None):
    try:
        import streamlit as st
        return st.secrets.get(key, default)
    except Exception:
        return default

WP_URL = _get_secret('WP_URL')
WP_USER = _get_secret('WP_USER')
WP_PASSWORD = _get_secret('WP_PASSWORD')
OPENAI_API_KEY = _get_secret('OPENAI_API_KEY')
GOOGLE_SHEET_NAME = _get_secret('GOOGLE_SHEET_NAME', _get_secret('GOOGLE_SHEET'))
GOOGLE_SHEET_ID = _get_secret('GOOGLE_SHEET_ID')
CREDENTIALS_FILE = _get_secret('CREDENTIALS_FILE', 'credenciais_google.json')

# Validação das configurações obrigatórias
def validar_configuracoes():
    """Valida se todas as configurações necessárias estão definidas"""
    erros = []
    
    # Verificar OpenAI
    if not OPENAI_API_KEY or len(OPENAI_API_KEY) < 20:
        erros.append("OPENAI_API_KEY não está definida ou é inválida")
    
    # Verificar WordPress
    if not WP_PASSWORD or WP_PASSWORD in ['senha', 'sua_senha']:
        erros.append("WP_PASSWORD não está definida corretamente")
    
    if WP_URL in ['https://exemplo.com', 'https://seu-site.com']:
        erros.append("WP_URL não está configurada com seu site real")
    
    if erros:
        print("❌ Configurações faltando:")
        for erro in erros:
            print(f"  - {erro}")
        print("\n💡 Configure suas credenciais no Streamlit Secrets")
        return False
    
    return True