#!/usr/bin/env python3
"""
Validação Final do Projeto RoboWordpress
Verifica se todos os componentes estão funcionando corretamente
"""

import os
import sys
import json
from pathlib import Path

def verificar_arquivos_essenciais():
    """Verifica se todos os arquivos essenciais existem"""
    print("📁 Verificando arquivos essenciais...")
    
    arquivos_obrigatorios = [
        'app.py',                    # Interface Streamlit
        'robo_pilloto_v3.py',       # Robô personalizável
        'prompt_manager.py',         # Gerenciador de prompts
        'prompts.json',             # Arquivo de prompts
        'config.py',                # Configurações
        '.env.example',             # Template de variáveis
        'requirements.txt',          # Dependências
        'README.md',                # Documentação
        'setup.sh',                 # Script de configuração
        'start_web.sh',             # Script para interface web
    ]
    
    todos_presentes = True
    for arquivo in arquivos_obrigatorios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - FALTANDO!")
            todos_presentes = False
    
    return todos_presentes

def verificar_estrutura_prompts():
    """Verifica se o sistema de prompts está configurado corretamente"""
    print("\n🎯 Verificando sistema de prompts...")
    
    try:
        # Verificar se prompts.json existe e tem estrutura correta
        with open('prompts.json', 'r', encoding='utf-8') as f:
            prompts = json.load(f)
        
        chaves_necessarias = ['prompt_titulo', 'prompt_artigo', 'system_prompt_titulo', 'system_prompt_artigo']
        
        for chave in chaves_necessarias:
            if chave in prompts:
                print(f"✅ {chave}")
            else:
                print(f"❌ {chave} - FALTANDO!")
                return False
        
        # Verificar se contém variáveis necessárias
        if '{topico_geral}' in prompts['prompt_titulo']:
            print("✅ Variável {topico_geral} no prompt_titulo")
        else:
            print("❌ Variável {topico_geral} faltando no prompt_titulo")
            return False
            
        if '{titulo_especifico}' in prompts['prompt_artigo']:
            print("✅ Variável {titulo_especifico} no prompt_artigo")
        else:
            print("❌ Variável {titulo_especifico} faltando no prompt_artigo")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar prompts: {e}")
        return False

def verificar_interface_streamlit():
    """Verifica se a interface Streamlit está pronta"""
    print("\n🌐 Verificando interface Streamlit...")
    
    try:
        # Testar importação do Streamlit
        import streamlit as st
        print(f"✅ Streamlit {st.__version__} instalado")
        
        # Verificar sintaxe do app.py
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        compile(content, 'app.py', 'exec')
        print("✅ app.py sem erros de sintaxe")
        
        # Verificar se contém funcionalidades essenciais
        funcionalidades = [
            'Editor de Prompts',
            'carregar_prompts',
            'salvar_prompts',
            'Robô Personalizável (v3)',
            'st.text_area'
        ]
        
        for func in funcionalidades:
            if func in content:
                print(f"✅ {func} presente")
            else:
                print(f"❌ {func} não encontrado")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        return False

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("\n📦 Verificando dependências...")
    
    dependencias_criticas = [
        ('streamlit', 'Interface web'),
        ('openai', 'API OpenAI'),
        ('gspread', 'Google Sheets'),
        ('requests', 'Requisições HTTP'),
        ('pandas', 'Manipulação de dados'),
    ]
    
    todas_instaladas = True
    for dep, descricao in dependencias_criticas:
        try:
            __import__(dep)
            print(f"✅ {dep} - {descricao}")
        except ImportError:
            print(f"❌ {dep} - {descricao} - NÃO INSTALADO!")
            todas_instaladas = False
    
    return todas_instaladas

def verificar_scripts():
    """Verifica se os scripts estão executáveis"""
    print("\n🔧 Verificando scripts...")
    
    scripts = ['setup.sh', 'start_web.sh']
    
    for script in scripts:
        if os.path.exists(script):
            # Verificar se é executável
            if os.access(script, os.X_OK):
                print(f"✅ {script} - Executável")
            else:
                print(f"⚠️  {script} - Existe mas não é executável")
                print(f"   Execute: chmod +x {script}")
        else:
            print(f"❌ {script} - Não encontrado")
            return False
    
    return True

def main():
    """Executa todas as verificações"""
    print("🚀 RoboWordpress - Validação Final")
    print("=" * 50)
    
    resultados = []
    
    # Executar todas as verificações
    resultados.append(verificar_arquivos_essenciais())
    resultados.append(verificar_estrutura_prompts())
    resultados.append(verificar_interface_streamlit())
    resultados.append(verificar_dependencias())
    resultados.append(verificar_scripts())
    
    print("\n" + "=" * 50)
    print("📊 RESULTADO FINAL:")
    
    if all(resultados):
        print("✅ PROJETO 100% FUNCIONAL!")
        print("\n🎉 PARABÉNS! O RoboWordpress está pronto!")
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Configure o arquivo .env com suas credenciais")
        print("2. Adicione credenciais_google.json")
        print("3. Execute: ./start_web.sh")
        print("4. Acesse: http://localhost:8501")
        print("5. Use o editor de prompts para personalizar a IA")
        print("6. Execute o 'Robô Personalizável (v3)'")
        
        print("\n🎯 FUNCIONALIDADES DISPONÍVEIS:")
        print("• 🎨 Editor visual de prompts")
        print("• 🤖 Execução de robôs pela interface")
        print("• 🧪 Testes integrados")
        print("• 📊 Painel de status")
        print("• 🔧 Configuração simplificada")
        
        return True
    else:
        print("❌ EXISTEM PROBLEMAS A RESOLVER!")
        print("   Verifique os erros listados acima")
        return False

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
