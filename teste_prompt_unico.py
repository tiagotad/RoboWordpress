#!/usr/bin/env python3
"""
Teste rápido do novo sistema de prompt único
"""

import sys
sys.path.append('/Users/tiago/Projetos/RoboWordpress')

from prompt_manager import get_prompt_completo, get_system_prompt, carregar_prompts

def testar_prompts():
    print("=== TESTE DO SISTEMA DE PROMPT ÚNICO ===")
    print()
    
    # Carregar prompts
    prompts = carregar_prompts()
    print("📋 Prompts carregados:")
    for key, value in prompts.items():
        print(f"  ✅ {key}: {len(value)} caracteres")
    print()
    
    # Testar prompt completo
    topico_teste = "Filmes de terror 2025"
    
    print(f"🎯 Testando com tópico: '{topico_teste}'")
    print()
    
    try:
        prompt_completo = get_prompt_completo(topico_teste)
        system_prompt = get_system_prompt()
        
        print("📝 PROMPT COMPLETO:")
        print("-" * 50)
        print(prompt_completo[:500] + "..." if len(prompt_completo) > 500 else prompt_completo)
        print()
        
        print("🎭 SYSTEM PROMPT:")
        print("-" * 50)
        print(system_prompt[:300] + "..." if len(system_prompt) > 300 else system_prompt)
        print()
        
        print("✅ Testes OK! Sistema de prompt único funcionando")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    testar_prompts()
