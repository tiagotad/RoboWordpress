#!/usr/bin/env python3
"""
Demonstração do sistema de prompts personalizáveis
"""

from prompt_manager import carregar_prompts, salvar_prompts, get_prompt_titulo, get_prompt_artigo, get_system_prompts

def demonstrar_prompts():
    """Demonstra como o sistema de prompts funciona"""
    print("🎯 RoboWordpress - Sistema de Prompts Personalizáveis")
    print("=" * 60)
    
    # Carregar prompts atuais
    print("📋 Carregando prompts atuais...")
    prompts = carregar_prompts()
    
    print("\n📰 PROMPT PARA TÍTULOS:")
    print("-" * 40)
    print(prompts['prompt_titulo'][:200] + "..." if len(prompts['prompt_titulo']) > 200 else prompts['prompt_titulo'])
    
    print("\n📄 PROMPT PARA ARTIGOS:")
    print("-" * 40)
    print(prompts['prompt_artigo'][:200] + "..." if len(prompts['prompt_artigo']) > 200 else prompts['prompt_artigo'])
    
    print("\n🎭 SYSTEM PROMPTS:")
    print("-" * 40)
    print(f"Título: {prompts['system_prompt_titulo']}")
    print(f"Artigo: {prompts['system_prompt_artigo']}")
    
    # Demonstrar formatação
    print("\n🔧 EXEMPLO DE FORMATAÇÃO:")
    print("-" * 40)
    
    topico_exemplo = "Filmes e Cinema"
    titulo_exemplo = "Os 10 Filmes Mais Aguardados de 2025"
    
    print(f"📌 Tópico: {topico_exemplo}")
    print(f"📌 Título gerado: {titulo_exemplo}")
    
    print("\n📰 Prompt formatado para título:")
    prompt_titulo_formatado = get_prompt_titulo(topico_exemplo)
    print(prompt_titulo_formatado[:300] + "..." if len(prompt_titulo_formatado) > 300 else prompt_titulo_formatado)
    
    print("\n📄 Prompt formatado para artigo:")
    prompt_artigo_formatado = get_prompt_artigo(titulo_exemplo, topico_exemplo)
    print(prompt_artigo_formatado[:300] + "..." if len(prompt_artigo_formatado) > 300 else prompt_artigo_formatado)
    
    print("\n✨ COMO USAR:")
    print("-" * 40)
    print("1. 🌐 Abra a interface web: streamlit run app.py")
    print("2. 📝 Use o 'Editor de Prompts Personalizáveis'")
    print("3. ✏️  Edite os prompts conforme sua necessidade")
    print("4. 💾 Salve as alterações")
    print("5. 🤖 Execute o 'Robô Personalizável (v3)'")
    
    print("\n🎯 BENEFÍCIOS:")
    print("-" * 40)
    print("• ✏️  Controle total sobre como a IA gera conteúdo")
    print("• 🎨 Personalização do tom e estilo")
    print("• 🔧 Ajustes sem mexer no código")
    print("• 👁️  Preview das mudanças antes de salvar")
    print("• 🔄 Fácil restauração para prompts padrão")

if __name__ == "__main__":
    demonstrar_prompts()
