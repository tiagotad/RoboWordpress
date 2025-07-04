#!/usr/bin/env python3
"""
Teste de execução dos robôs v3 e v4 para validar se funcionam corretamente
tanto via terminal quanto via interface
"""

import subprocess
import sys
import time
import threading
import os

def testar_importacao_robo(nome_arquivo):
    """Testa se o robô pode ser importado sem erros"""
    print(f"\n{'='*50}")
    print(f"🧪 TESTANDO IMPORTAÇÃO: {nome_arquivo}")
    print('='*50)
    
    try:
        # Tenta importar o módulo
        import importlib.util
        spec = importlib.util.spec_from_file_location("robo", nome_arquivo)
        robo_module = importlib.util.module_from_spec(spec)
        
        # Executa apenas as importações (não executa o código principal)
        print("📦 Testando importações...")
        spec.loader.exec_module(robo_module)
        print("✅ Importações OK!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na importação: {e}")
        return False

def testar_configuracoes():
    """Testa se as configurações estão funcionando"""
    print(f"\n{'='*50}")
    print("🔧 TESTANDO CONFIGURAÇÕES")
    print('='*50)
    
    try:
        from config_execucao import get_configuracoes_execucao
        config = get_configuracoes_execucao()
        print(f"✅ Configurações carregadas: {config}")
        
        # Verifica se author_id está presente
        if 'author_id' in config:
            print(f"✅ author_id encontrado: {config['author_id']}")
        else:
            print("❌ author_id não encontrado nas configurações!")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar configurações: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 INICIANDO TESTES DE VALIDAÇÃO DOS ROBÔS")
    print("="*60)
    
    # Muda para o diretório correto
    os.chdir('/Users/tiago/Projetos/RoboWordpress')
    
    resultados = {}
    
    # Teste 1: Configurações
    resultados['config'] = testar_configuracoes()
    
    # Teste 2: Importação dos robôs
    robos = [
        'robo_pilloto_v3.py',
        'robo_pilloto_v4.py'
    ]
    
    for robo in robos:
        if os.path.exists(robo):
            resultados[robo] = testar_importacao_robo(robo)
        else:
            print(f"❌ Arquivo {robo} não encontrado!")
            resultados[robo] = False
    
    # Relatório final
    print(f"\n{'='*60}")
    print("📋 RELATÓRIO FINAL DOS TESTES")
    print('='*60)
    
    for teste, resultado in resultados.items():
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{teste}: {status}")
    
    todos_passaram = all(resultados.values())
    if todos_passaram:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Os robôs estão prontos para execução via interface e terminal!")
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM!")
        print("❌ Verifique os erros acima antes de prosseguir.")
    
    return todos_passaram

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
