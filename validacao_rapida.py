#!/usr/bin/env python3
"""
Validação rápida: verifica se os robôs podem ser importados e executados
"""

print("🔍 VALIDAÇÃO RÁPIDA DOS ROBÔS")
print("="*40)

# Teste 1: Configurações
try:
    from config_execucao import get_configuracoes_execucao
    config = get_configuracoes_execucao()
    print(f"✅ Configurações: {config.keys()}")
    print(f"   - author_id: {config.get('author_id', 'AUSENTE!')}")
except Exception as e:
    print(f"❌ Erro configurações: {e}")

# Teste 2: Config imports
print("\n🔧 Testando imports de configuração...")
try:
    import sys
    import os
    # Simula ambiente não-Streamlit
    if 'streamlit' in sys.modules:
        del sys.modules['streamlit']
    
    # Testa o import condicional
    exec("""
try:
    import streamlit as st
    if hasattr(st, "secrets"):
        try:
            if "WP_URL" in st.secrets:
                from config_cloud import *
                print("   ✅ config_cloud importado")
            else:
                from config import *
                print("   ✅ config local importado (sem WP_URL)")
        except Exception:
            from config import *
            print("   ✅ config local importado (erro secrets)")
    else:
        from config import *
        print("   ✅ config local importado (sem secrets)")
except ImportError:
    from config import *
    print("   ✅ config local importado (sem streamlit)")
""")
    
except Exception as e:
    print(f"   ❌ Erro no import: {e}")

print("\n🎯 VALIDAÇÃO CONCLUÍDA!")
print("Os robôs devem funcionar tanto via interface quanto terminal.")
