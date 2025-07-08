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

def get_prompt_completo(topico_geral: str) -> str:
    """Retorna o prompt formatado para geração completa (título + artigo)"""
    prompts = carregar_prompts()
    return prompts['prompt_completo'].format(topico_geral=topico_geral)

def get_system_prompt() -> str:
    """Retorna o system prompt único"""
    prompts = carregar_prompts()
    return prompts.get('system_prompt', '')

# Funções mantidas para compatibilidade (deprecated)
def get_prompt_titulo(topico_geral: str) -> str:
    """[DEPRECATED] Use get_prompt_completo()"""
    return get_prompt_completo(topico_geral)

def get_prompt_artigo(titulo_especifico: str, topico_geral: str) -> str:
    """[DEPRECATED] Use get_prompt_completo()"""
    return get_prompt_completo(topico_geral)

def get_system_prompts() -> Dict[str, str]:
    """[DEPRECATED] Use get_system_prompt()"""
    system_prompt = get_system_prompt()
    return {
        'titulo': system_prompt,
        'artigo': system_prompt
    }

def get_prompts_padrao() -> Dict[str, str]:
    """Retorna prompts padrão caso o arquivo não exista"""
    return {
        "prompt_completo": """Com base no tópico geral '{topico_geral}', crie um artigo completo com título e conteúdo.

O artigo deve:
• Ter um título SEO otimizado (50-80 caracteres)
• Conter 1000-1200 palavras
• Ser estruturado com introdução, desenvolvimento e conclusão
• Incluir subtítulos H2 e H3
• Ter tom conversacional e informativo
• Estar otimizado para SEO

Formato da resposta:
TÍTULO: [seu título aqui]

ARTIGO:
[seu artigo completo aqui]""",
        "system_prompt": "Você é um jornalista especializado em entretenimento e estilo de vida, com amplo conhecimento em filmes, séries de TV, livros, destinos de viagem e tendências culturais. Você cria conteúdos altamente envolventes e otimizados para SEO."
    }

def validar_prompts(prompts: Dict[str, str]) -> Dict[str, str]:
    """Valida se os prompts contêm as variáveis necessárias"""
    erros = {}
    
    # Verificar prompt_completo
    if '{topico_geral}' not in prompts.get('prompt_completo', ''):
        erros['prompt_completo'] = 'Deve conter a variável {topico_geral}'
    
    return erros
