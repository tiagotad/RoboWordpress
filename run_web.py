#!/usr/bin/env python3
"""
Script para iniciar a interface web do RoboWordpress com foco nos prompts
"""
import subprocess
import sys
import os

def main():
    # Mudar para o diretório correto
    os.chdir('/Users/tiago/Projetos/RoboWordpress')
    
    print("🚀 Iniciando RoboWordpress Web Interface...")
    print("📂 Diretório:", os.getcwd())
    
    # Verificar se arquivos existem
    if not os.path.exists('app.py'):
        print("❌ Erro: app.py não encontrado!")
        return
    
    if not os.path.exists('venv'):
        print("❌ Erro: Ambiente virtual não encontrado!")
        return
    
    if not os.path.exists('prompt_manager.py'):
        print("❌ Erro: prompt_manager.py não encontrado!")
        return
        
    if not os.path.exists('prompts.json'):
        print("⚠️  Arquivo prompts.json não encontrado, será criado automaticamente")
    
    print("✅ Arquivos encontrados")
    print("� Interface com editor de prompts personalizáveis")
    print("�🌐 Iniciando Streamlit em http://localhost:8501")
    print("🛑 Para parar: Ctrl+C")
    print("-" * 50)
    
    # Comandos para executar
    activate_venv = "source venv/bin/activate"
    run_streamlit = "streamlit run app.py --server.port 8501 --server.address localhost"
    
    # Executar comando completo
    full_command = f"{activate_venv} && {run_streamlit}"
    
    try:
        # Executar em shell
        subprocess.run(full_command, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Interface web encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
        print("\n💡 Dica: Tente executar manualmente:")
        print("cd /Users/tiago/Projetos/RoboWordpress")
        print("source venv/bin/activate")
        print("streamlit run app.py")

if __name__ == "__main__":
    main()
