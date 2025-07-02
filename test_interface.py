#!/usr/bin/env python3
"""
Script de teste para verificar se a interface web está funcionando corretamente
"""

import sys
import subprocess
import time
import requests
import threading
from prompt_manager import carregar_prompts, salvar_prompts, get_prompts_padrao

def testar_prompt_manager():
    """Testa as funcionalidades do prompt manager"""
    print("🧪 Testando prompt manager...")
    
    try:
        # Testar carregamento de prompts
        prompts = carregar_prompts()
        print(f"✅ Prompts carregados: {len(prompts)} itens")
        
        # Verificar se contém as chaves necessárias
        chaves_esperadas = ['prompt_titulo', 'prompt_artigo', 'system_prompt_titulo', 'system_prompt_artigo']
        for chave in chaves_esperadas:
            if chave in prompts:
                print(f"✅ Chave '{chave}' encontrada")
            else:
                print(f"❌ Chave '{chave}' não encontrada")
                return False
        
        # Testar salvamento (backup atual)
        prompts_backup = prompts.copy()
        
        # Testar com prompts de teste
        prompts_teste = {
            'prompt_titulo': 'Teste título: {topico_geral}',
            'prompt_artigo': 'Teste artigo: {titulo_especifico} sobre {topico_geral}',
            'system_prompt_titulo': 'Teste system título',
            'system_prompt_artigo': 'Teste system artigo'
        }
        
        if salvar_prompts(prompts_teste):
            print("✅ Salvamento de prompts funcionando")
            
            # Restaurar backup
            salvar_prompts(prompts_backup)
            print("✅ Backup restaurado")
        else:
            print("❌ Erro no salvamento")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no prompt manager: {e}")
        return False

def testar_streamlit():
    """Testa se o Streamlit pode ser executado"""
    print("🧪 Testando se Streamlit pode ser executado...")
    
    try:
        # Testar importação
        import streamlit as st
        print(f"✅ Streamlit importado: versão {st.__version__}")
        
        # Testar se app.py não tem erros de sintaxe
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        compile(app_content, 'app.py', 'exec')
        print("✅ app.py não tem erros de sintaxe")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no Streamlit: {e}")
        return False

def testar_dependencias():
    """Testa se todas as dependências estão instaladas"""
    print("🧪 Testando dependências...")
    
    dependencias = [
        'streamlit',
        'pandas', 
        'requests',
        'openai',
        'gspread',
        'google.oauth2.service_account'
    ]
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep} disponível")
        except ImportError:
            print(f"❌ {dep} não encontrado")
            return False
    
    return True

def main():
    """Executa todos os testes"""
    print("🤖 RoboWordpress - Teste da Interface Web")
    print("=" * 50)
    
    resultados = []
    
    # Teste 1: Dependências
    resultados.append(testar_dependencias())
    
    # Teste 2: Prompt Manager
    resultados.append(testar_prompt_manager())
    
    # Teste 3: Streamlit
    resultados.append(testar_streamlit())
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    
    if all(resultados):
        print("✅ TODOS OS TESTES PASSARAM!")
        print("\n🚀 A interface web está pronta para uso:")
        print("   Execute: streamlit run app.py")
        print("\n💡 Recursos disponíveis:")
        print("   - Editor visual de prompts")
        print("   - Execução dos robôs")
        print("   - Testes de conexão")
        print("   - Painel de status")
        return True
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("   Verifique os erros acima antes de usar a interface")
        return False

if __name__ == "__main__":
    main()
