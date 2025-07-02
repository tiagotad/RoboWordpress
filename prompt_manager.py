"""
Módulo para gerenciar prompts do RoboWordpress
"""
import json
import os
from typing import Dict, Any

PROMPTS_FILE = 'prompts.json'

def carregar_prompts() -> Dict[str, str]:
    """Carrega os prompts do arquivo JSON"""
    try:
        if os.path.exists(PROMPTS_FILE):
            with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Retorna prompts padrão se o arquivo não existir
            return get_prompts_padrao()
    except Exception as e:
        print(f"Erro ao carregar prompts: {e}")
        return get_prompts_padrao()

def salvar_prompts(prompts: Dict[str, str]) -> bool:
    """Salva os prompts no arquivo JSON"""
    try:
        with open(PROMPTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar prompts: {e}")
        return False

def get_prompt_titulo(topico_geral: str) -> str:
    """Retorna o prompt formatado para geração de título"""
    prompts = carregar_prompts()
    return prompts['prompt_titulo'].format(topico_geral=topico_geral)

def get_prompt_artigo(titulo_especifico: str, topico_geral: str) -> str:
    """Retorna o prompt formatado para geração de artigo"""
    prompts = carregar_prompts()
    return prompts['prompt_artigo'].format(
        titulo_especifico=titulo_especifico,
        topico_geral=topico_geral
    )

def get_system_prompts() -> Dict[str, str]:
    """Retorna os system prompts"""
    prompts = carregar_prompts()
    return {
        'titulo': prompts.get('system_prompt_titulo', ''),
        'artigo': prompts.get('system_prompt_artigo', '')
    }

def get_prompts_padrao() -> Dict[str, str]:
    """Retorna prompts padrão caso o arquivo não exista"""
    return {
        "prompt_titulo": "Crie um título SEO otimizado sobre '{topico_geral}'. Retorne apenas o título.",
        "prompt_artigo": "Escreva um artigo sobre '{titulo_especifico}' relacionado ao tópico '{topico_geral}'.",
        "system_prompt_titulo": "Você é um especialista em SEO e criação de títulos.",
        "system_prompt_artigo": "Você é um redator especializado em conteúdo para blogs."
    }

def validar_prompts(prompts: Dict[str, str]) -> Dict[str, str]:
    """Valida se os prompts contêm as variáveis necessárias"""
    erros = {}
    
    # Verificar prompt_titulo
    if '{topico_geral}' not in prompts.get('prompt_titulo', ''):
        erros['prompt_titulo'] = 'Deve conter a variável {topico_geral}'
    
    # Verificar prompt_artigo
    prompt_artigo = prompts.get('prompt_artigo', '')
    if '{titulo_especifico}' not in prompt_artigo:
        erros['prompt_artigo'] = 'Deve conter a variável {titulo_especifico}'
    
    return erros
