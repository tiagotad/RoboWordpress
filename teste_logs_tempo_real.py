#!/usr/bin/env python3
"""
Script de teste para demonstrar logs em tempo real
"""

import time
import sys

def teste_logs_tempo_real():
    """Simula execução com múltiplas etapas para testar logs"""
    
    print("🔄 Iniciando teste de logs em tempo real...")
    time.sleep(1)
    
    print("📋 Carregando configurações...")
    time.sleep(1)
    
    print("🔗 Conectando com APIs...")
    time.sleep(2)
    
    print("✅ Conexão estabelecida com sucesso!")
    time.sleep(1)
    
    print("📝 Processando dados...")
    for i in range(1, 6):
        print(f"   - Processando item {i}/5...")
        time.sleep(1)
    
    print("🚀 Executando ação principal...")
    time.sleep(2)
    
    print("💾 Salvando resultados...")
    time.sleep(1)
    
    print("🎉 Processo concluído com sucesso!")
    print("📊 Resultados:")
    print("   - 5 itens processados")
    print("   - 0 erros encontrados")
    print("   - Tempo total: ~10 segundos")

if __name__ == "__main__":
    try:
        teste_logs_tempo_real()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro durante execução: {str(e)}")
        sys.exit(1)
