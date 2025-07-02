#!/usr/bin/env python3
"""
Script para testar rapidamente a interface Streamlit
"""

import subprocess
import time
import sys
import requests
import threading
import signal
import os

def test_streamlit_startup():
    """Testa se o Streamlit inicia corretamente"""
    print("🧪 Testando inicialização do Streamlit...")
    
    try:
        # Iniciar o Streamlit em processo separado
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--server.address", "localhost"
        ], 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
        
        # Aguardar um pouco para o servidor iniciar
        print("⏳ Aguardando servidor iniciar...")
        time.sleep(8)
        
        # Testar se o servidor está respondendo
        try:
            response = requests.get("http://localhost:8501", timeout=5)
            print(f"✅ Servidor Streamlit respondendo: {response.status_code}")
            success = True
        except requests.exceptions.RequestException as e:
            print(f"❌ Servidor não está respondendo: {e}")
            success = False
        
        # Finalizar o processo
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        
        return success
        
    except Exception as e:
        print(f"❌ Erro ao testar Streamlit: {e}")
        return False

def main():
    print("🔬 Teste Rápido da Interface Streamlit")
    print("=" * 40)
    
    if test_streamlit_startup():
        print("\n✅ INTERFACE STREAMLIT FUNCIONANDO!")
        print("\n🚀 Para usar a interface:")
        print("   streamlit run app.py")
        print("\n🌐 Acesse: http://localhost:8501")
        print("\n📝 Recursos disponíveis:")
        print("   • Editor visual de prompts")
        print("   • Execução dos robôs")
        print("   • Testes de conexão") 
        print("   • Monitoramento de status")
    else:
        print("\n❌ PROBLEMA NA INTERFACE!")
        print("   Verifique os logs acima")

if __name__ == "__main__":
    main()
