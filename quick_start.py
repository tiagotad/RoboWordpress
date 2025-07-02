#!/usr/bin/env python3
"""
Teste da interface web do RoboWordpress
"""
import subprocess
import time
import webbrowser
import os

def main():
    print("🧪 Testando interface web do RoboWordpress...")
    
    # Mudar para o diretório correto
    os.chdir('/Users/tiago/Projetos/RoboWordpress')
    
    print("📂 Diretório atual:", os.getcwd())
    
    # Verificar arquivos necessários
    arquivos = ['app.py', 'prompt_manager.py', 'prompts.json', 'config.py']
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} - OK")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
    
    print("\n🚀 Iniciando Streamlit...")
    print("🌐 URL: http://localhost:8501")
    print("🛑 Para parar: Ctrl+C")
    print("-" * 50)
    
    try:
        # Executar streamlit
        comando = "source venv/bin/activate && streamlit run app.py --server.port 8501 --server.address localhost"
        
        # Abrir navegador após 3 segundos
        import threading
        def abrir_browser():
            time.sleep(3)
            webbrowser.open('http://localhost:8501')
        
        threading.Thread(target=abrir_browser, daemon=True).start()
        
        # Executar comando
        subprocess.run(comando, shell=True, check=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Interface web encerrada")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
