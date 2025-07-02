#!/usr/bin/env python3
"""
Teste rápido das configurações do RoboWordpress
"""

import os
import sys

# Importar configurações
from config import WP_URL, WP_USER, WP_PASSWORD, OPENAI_API_KEY, GOOGLE_SHEET_NAME, GOOGLE_SHEET_ID, validar_configuracoes

def testar_configuracoes():
    """Testa se as configurações estão sendo carregadas corretamente"""
    print("🔧 Testando configurações do RoboWordpress...")
    print("=" * 50)
    
    try:
        print("📋 Configurações carregadas:")
        print(f"✅ WP_URL: {WP_URL}")
        print(f"✅ WP_USER: {WP_USER}")
        print(f"✅ WP_PASSWORD: {'*' * len(WP_PASSWORD) if WP_PASSWORD else 'NÃO DEFINIDA'}")
        print(f"✅ OPENAI_API_KEY: {OPENAI_API_KEY[:20]}..." if OPENAI_API_KEY else "❌ NÃO DEFINIDA")
        print(f"✅ GOOGLE_SHEET_NAME: {GOOGLE_SHEET_NAME}")
        print(f"✅ GOOGLE_SHEET_ID: {GOOGLE_SHEET_ID[:15]}..." if GOOGLE_SHEET_ID else "❌ NÃO DEFINIDA")
        
        print("\n🧪 Testando validação...")
        if validar_configuracoes():
            print("✅ TODAS AS CONFIGURAÇÕES ESTÃO OK!")
            return True
        else:
            print("❌ ALGUMAS CONFIGURAÇÕES ESTÃO FALTANDO")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")
        return False

def testar_arquivos():
    """Verifica se arquivos necessários existem"""
    print("\n📁 Verificando arquivos...")
    
    arquivos = [
        'config.py',
        'prompt_manager.py', 
        'prompts.json',
        'app.py'
    ]
    
    todos_ok = True
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - FALTANDO!")
            todos_ok = False
    
    # Verificar credenciais Google (opcional)
    if os.path.exists('credenciais_google.json'):
        print("✅ credenciais_google.json")
    else:
        print("⚠️  credenciais_google.json - Não encontrado (pode estar nos secrets)")
    
    return todos_ok

if __name__ == "__main__":
    print("🤖 RoboWordpress - Teste de Configurações")
    print("=" * 50)
    
    # Testar arquivos
    arquivos_ok = testar_arquivos()
    
    # Testar configurações
    config_ok = testar_configuracoes()
    
    print("\n" + "=" * 50)
    print("📊 RESULTADO FINAL:")
    
    if arquivos_ok and config_ok:
        print("✅ TUDO OK! O RoboWordpress está pronto para usar!")
        print("\n🚀 Para usar:")
        print("  - Interface web: streamlit run app.py")
        print("  - Robô personalizado: python robo_pilloto_v3.py")
    else:
        print("❌ PROBLEMAS ENCONTRADOS!")
        print("📋 Verifique os erros acima e configure as credenciais")
        
        if not config_ok:
            print("\n💡 Como configurar:")
            print("  - Local: edite o arquivo .env")
            print("  - Streamlit Cloud: configure na seção Secrets")
