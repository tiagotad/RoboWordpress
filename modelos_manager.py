# Gerenciador de modelos salvos (prompts e tópicos)
import json
import os
from datetime import datetime

MODELOS_FILE = "modelos_salvos.json"

def carregar_modelos():
    """Carrega modelos salvos do arquivo JSON"""
    try:
        if os.path.exists(MODELOS_FILE):
            with open(MODELOS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"prompts": {}, "topicos": {}}
    except Exception as e:
        print(f"Erro ao carregar modelos: {e}")
        return {"prompts": {}, "topicos": {}}

def salvar_modelos(modelos):
    """Salva modelos no arquivo JSON"""
    try:
        with open(MODELOS_FILE, 'w', encoding='utf-8') as f:
            json.dump(modelos, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar modelos: {e}")
        return False

def salvar_modelo_prompt(nome, prompts):
    """Salva um modelo de prompt"""
    modelos = carregar_modelos()
    
    modelo = {
        "prompt_titulo": prompts.get('prompt_titulo', ''),
        "prompt_artigo": prompts.get('prompt_artigo', ''),
        "system_prompt_titulo": prompts.get('system_prompt_titulo', ''),
        "system_prompt_artigo": prompts.get('system_prompt_artigo', ''),
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    modelos["prompts"][nome] = modelo
    return salvar_modelos(modelos)

def salvar_modelo_topicos(nome, topicos_lista):
    """Salva um modelo de tópicos"""
    modelos = carregar_modelos()
    
    modelo = {
        "topicos": topicos_lista,
        "quantidade": len(topicos_lista),
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    modelos["topicos"][nome] = modelo
    return salvar_modelos(modelos)

def carregar_modelo_prompt(nome):
    """Carrega um modelo de prompt específico"""
    modelos = carregar_modelos()
    return modelos["prompts"].get(nome, None)

def carregar_modelo_topicos(nome):
    """Carrega um modelo de tópicos específico"""
    modelos = carregar_modelos()
    return modelos["topicos"].get(nome, None)

def listar_modelos_prompts():
    """Lista todos os modelos de prompts salvos"""
    modelos = carregar_modelos()
    return list(modelos["prompts"].keys())

def listar_modelos_topicos():
    """Lista todos os modelos de tópicos salvos"""
    modelos = carregar_modelos()
    return list(modelos["topicos"].keys())

def deletar_modelo_prompt(nome):
    """Deleta um modelo de prompt"""
    modelos = carregar_modelos()
    if nome in modelos["prompts"]:
        del modelos["prompts"][nome]
        return salvar_modelos(modelos)
    return False

def deletar_modelo_topicos(nome):
    """Deleta um modelo de tópicos"""
    modelos = carregar_modelos()
    if nome in modelos["topicos"]:
        del modelos["topicos"][nome]
        return salvar_modelos(modelos)
    return False

def get_modelos_predefinidos():
    """Retorna modelos predefinidos para inicialização"""
    return {
        "prompts": {
            "Blog Entretenimento": {
                "prompt_titulo": """Você é um especialista em criação de conteúdo para entretenimento e estilo de vida. Com base no tópico geral "{topico_geral}", crie UM título específico e otimizado para SEO em Português, voltado para blog.

O título deve:
• Focar em tendências recentes, notícias ou acontecimentos nas áreas de: filmes, séries, livros, viagens, história ou cultura pop
• Basear-se em eventos atuais de fontes confiáveis como IMDb, Netflix, Amazon Prime, Disney+, grandes editoras, sites de viagem ou descobertas históricas
• Ser altamente pesquisável e atrativo para SEO
• Ter como público-alvo entusiastas do entretenimento e o público geral
• Ter entre 50 e 80 caracteres, ideal para SEO
• Incluir palavras-chave que estão em alta nas buscas

Exemplos de bons títulos:
- "As séries mais assistidas da Netflix em 2024: Guia completo"
- "10 filmes que estreiam em 2025 e que todo mundo vai comentar"
- "As histórias reais por trás de 5 documentários criminais da Netflix"

Retorne APENAS o título, nada mais.""",
                "system_prompt_titulo": "Você é um jornalista especializado em entretenimento e estrategista de conteúdo SEO, com profundo conhecimento em filmes, séries de TV, livros, viagens e tendências da cultura pop.",
                "prompt_artigo": """Escreva um post de blog completo e otimizado para SEO com 1000 a 1200 palavras, intitulado: "{titulo_especifico}"

ESTRUTURA DO ARTIGO E REQUISITOS DE SEO:
1. Introdução Atrativa (150–200 palavras):
• Comece com um fato envolvente, estatística ou evento recente
• Inclua a palavra-chave principal naturalmente no primeiro parágrafo
• Deixe claro o que o leitor aprenderá no artigo

2. Conteúdo Principal (700–800 palavras):
• Use subtítulos H2 e H3 com palavras-chave
• Divida o conteúdo em 3 ou 4 seções principais
• Use listas com marcadores e numeradas
• Adicione dados específicos, datas, nomes e estatísticas

3. Conclusão Envolvente (100–150 palavras):
• Resuma os principais pontos do artigo
• Inclua uma chamada para ação ou uma pergunta para engajamento

TOM E ESTILO:
• Conversacional e informativo
• Entusiástico sobre o tema
• Acessível para o público geral
• Use elementos de storytelling (narrativa)

Foco do tópico: {topico_geral}

Torne o conteúdo envolvente, informativo e altamente compartilhável, mantendo as melhores práticas de SEO.""",
                "system_prompt_artigo": "Você é um jornalista especializado em entretenimento e estilo de vida, com amplo conhecimento em filmes, séries de TV, livros, destinos de viagem e tendências culturais. Você cria conteúdos altamente envolventes e otimizados para SEO.",
                "data_criacao": "2025-07-02 16:00:00"
            }
        },
        "topicos": {
            "Entretenimento Geral": {
                "topicos": [
                    "Filmes e Cinema",
                    "Séries de TV",
                    "História e Curiosidades",
                    "Viagem e Turismo",
                    "Livros e Literatura"
                ],
                "quantidade": 5,
                "data_criacao": "2025-07-02 16:00:00"
            },
            "Tecnologia": {
                "topicos": [
                    "Inteligência Artificial",
                    "Smartphones e Gadgets",
                    "Programação e Desenvolvimento",
                    "Cibersegurança",
                    "Tendências Tech"
                ],
                "quantidade": 5,
                "data_criacao": "2025-07-02 16:00:00"
            },
            "Saúde e Bem-estar": {
                "topicos": [
                    "Exercícios e Fitness",
                    "Alimentação Saudável",
                    "Saúde Mental",
                    "Medicina Alternativa",
                    "Longevidade"
                ],
                "quantidade": 5,
                "data_criacao": "2025-07-02 16:00:00"
            }
        }
    }
