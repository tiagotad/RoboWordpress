#!/usr/bin/env python3
"""
Teste rápido do sistema de prompts personalizáveis
"""
import sys
import os

# Adicionar diretório atual ao path
sys.path.append(os.getcwd())

def testar_prompts():
    print("🧪 Testando sistema de prompts personalizáveis...")
    
    try:
        from prompt_manager import carregar_prompts, get_prompt_titulo, get_prompt_artigo, validar_prompts
        
        print("✅ Módulo prompt_manager importado com sucesso")
        
        # Testar carregamento de prompts
        prompts = carregar_prompts()
        print(f"✅ Prompts carregados: {len(prompts)} encontrados")
        
        # Testar validação
        erros = validar_prompts(prompts)
        if erros:
            print(f"⚠️  Erros de validação: {erros}")
        else:
            print("✅ Prompts válidos")
        
        # Testar formatação
        exemplo_topico = "Filmes e Cinema"
        exemplo_titulo = "Os 10 Filmes Mais Aguardados de 2025"
        
        prompt_titulo = get_prompt_titulo(exemplo_topico)
        prompt_artigo = get_prompt_artigo(exemplo_titulo, exemplo_topico)
        
        print(f"✅ Prompt título formatado: {len(prompt_titulo)} caracteres")
        print(f"✅ Prompt artigo formatado: {len(prompt_artigo)} caracteres")
        
        print("\n🎯 Preview do prompt título:")
        print("-" * 50)
        print(prompt_titulo[:200] + "..." if len(prompt_titulo) > 200 else prompt_titulo)
        print("-" * 50)
        
        print("\n📄 Preview do prompt artigo:")
        print("-" * 50)
        print(prompt_artigo[:300] + "..." if len(prompt_artigo) > 300 else prompt_artigo)
        print("-" * 50)
        
        print("\n🎉 Teste concluído com sucesso!")
        print("💡 Agora você pode usar a interface web para editar os prompts.")
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Verifique se o arquivo prompt_manager.py existe")
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")

if __name__ == "__main__":
    testar_prompts()
