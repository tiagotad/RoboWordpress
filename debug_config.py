#!/usr/bin/env python3
import sys
import os
sys.path.append('.')
from config import *

print('=== VERIFICAÇÃO DE CONFIGURAÇÕES ===')
print(f'WP_URL: {WP_URL}')
print(f'WP_PASSWORD: {"*" * len(WP_PASSWORD) if WP_PASSWORD else "VAZIO"}')
print(f'OPENAI_API_KEY: {OPENAI_API_KEY[:20]}...' if OPENAI_API_KEY else 'VAZIO')
print(f'GOOGLE_SHEET_ID: {GOOGLE_SHEET_ID}')

# Testar as validações
wp_ok = WP_URL not in ['https://exemplo.com', 'https://seu-site.com'] and WP_PASSWORD not in ['senha', 'sua_senha']
openai_ok = OPENAI_API_KEY and len(OPENAI_API_KEY) > 20 and OPENAI_API_KEY.startswith('sk-')
sheets_ok = (GOOGLE_SHEET_NAME not in ['nome_da_sua_planilha', 'TopicosBlog']) or bool(GOOGLE_SHEET_ID)
credentials_ok = os.path.exists('credenciais_google.json')

print()
print('=== RESULTADO DAS VALIDAÇÕES ===')
print(f'WordPress OK: {wp_ok}')
print(f'OpenAI OK: {openai_ok}')
print(f'Sheets OK: {sheets_ok}')
print(f'Credentials OK: {credentials_ok}')
print(f'TODOS OK: {wp_ok and openai_ok and sheets_ok and credentials_ok}')

print()
print('=== DETALHES DAS VERIFICAÇÕES ===')
print(f'WP_URL não é exemplo: {WP_URL not in ["https://exemplo.com", "https://seu-site.com"]}')
print(f'WP_PASSWORD não é padrão: {WP_PASSWORD not in ["senha", "sua_senha"]}')
print(f'OPENAI_API_KEY tem tamanho: {len(OPENAI_API_KEY) if OPENAI_API_KEY else 0}')
print(f'OPENAI_API_KEY começa com sk-: {OPENAI_API_KEY.startswith("sk-") if OPENAI_API_KEY else False}')
print(f'GOOGLE_SHEET_NAME: {GOOGLE_SHEET_NAME}')
print(f'GOOGLE_SHEET_NAME não é padrão: {GOOGLE_SHEET_NAME not in ["nome_da_sua_planilha", "TopicosBlog"]}')
print(f'GOOGLE_SHEET_ID existe: {bool(GOOGLE_SHEET_ID)}')
