# 1. Importar as bibliotecas necessárias
import sys
import os
import requests
import time
import os
from openai import OpenAI
from requests.auth import HTTPBasicAuth
import gspread
from google.oauth2.service_account import Credentials


# Importação condicional de configuração (local ou cloud)
try:
    import streamlit as st
    if hasattr(st, "secrets") and "WP_URL" in st.secrets:
        from config_cloud import *
        st.info(f"[DEBUG] Ambiente: Streamlit Cloud (config_cloud)\nChaves em st.secrets: {list(st.secrets.keys())}\nGOOGLE_CREDENTIALS_JSON está em st.secrets? {'GOOGLE_CREDENTIALS_JSON' in st.secrets}")
    else:
        from config import *
        st.info("[DEBUG] Ambiente: Local (config)")
except ImportError:
    from config import *
    print("[DEBUG] Ambiente: Local (config) - streamlit não disponível")

from prompt_manager import get_prompt_titulo, get_prompt_artigo, get_system_prompts

# Validar configurações ao iniciar


# Debug: ver de onde está vindo a chave OPENAI_API_KEY
try:
    origem = "st.secrets" if ('st' in globals() and hasattr(st, 'secrets') and 'OPENAI_API_KEY' in st.secrets) else "config.py/.env"
    print(f"[DEBUG] Origem da OPENAI_API_KEY: {origem}")
    print(f"[DEBUG] Valor da OPENAI_API_KEY (primeiros 8 chars): {OPENAI_API_KEY[:8]}")
except Exception as e:
    print(f"[DEBUG] Erro ao checar origem da OPENAI_API_KEY: {e}")

# Inicializar cliente OpenAI com configurações atualizadas
client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=30.0,  # Timeout de 30 segundos
    max_retries=3   # Máximo 3 tentativas
)

print("\n--- CARREGANDO TÓPICOS DO GOOGLE SHEETS ---")

# === CARREGAR TÓPICOS DO GOOGLE SHEETS ===
def carregar_topicos_sheets():
    try:
        print("Configurando credenciais...")
        # Configurar credenciais do Google Sheets
        scope = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        import json
        # Cloud: usar JSON das credenciais do secrets
        if 'st' in globals() and hasattr(st, 'secrets') and 'GOOGLE_CREDENTIALS_JSON' in st.secrets:
            creds_dict = json.loads(st.secrets['GOOGLE_CREDENTIALS_JSON'])
            creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        else:
            # Local: usar arquivo físico
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"[AVISO] Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}")
                return []
            creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
        gc = gspread.authorize(creds)
        
        print("Abrindo planilha...")
        # Abrir a planilha
        sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
        
        print("Lendo tópicos das células A2 até A4...")
        # Ler valores das células A2 até A4
        topicos = []
        for row in range(2, 5):  # Linhas 2, 3, 4
            try:
                cell_value = sheet.cell(row, 1).value  # Coluna A
                if cell_value and cell_value.strip():
                    topicos.append(cell_value.strip())
                    print(f"  Tópico encontrado na linha {row}: {cell_value.strip()}")
            except Exception as e:
                print(f"[AVISO] Erro ao ler linha {row}: {e}")
                continue
        
        return topicos
        
    except Exception as e:
        print(f"[ERRO] Não foi possível carregar tópicos do Google Sheets: {e}")
        print(f"Detalhes do erro: {type(e).__name__}")
        return []

topicos = carregar_topicos_sheets()

# Se não conseguir carregar do Google Sheets, usar tópicos padrão
if not topicos:
    print("[AVISO] Usando tópicos padrão pois não foi possível carregar da planilha")
    topicos = [
        "Filmes e Cinema",
        "Séries de TV", 
        "História e Curiosidades",
        "Viagem e Turismo",
        "Livros e Literatura"
    ]

# Importar configurações de execução
try:
    from config_execucao import get_configuracoes_execucao
    config_execucao = get_configuracoes_execucao()
    print(f"[INFO] Configurações de execução: {config_execucao}")
except ImportError:
    print("[AVISO] Arquivo config_execucao.py não encontrado, usando configurações padrão")
    config_execucao = {
        'categoria_wp': 'Others',
        'status_publicacao': 'draft',
        'quantidade_textos': 3
    }

# Limitar quantidade de tópicos conforme configuração
quantidade_maxima = config_execucao.get('quantidade_textos', 3)
if len(topicos) > quantidade_maxima:
    topicos = topicos[:quantidade_maxima]
    print(f"[INFO] Limitando execução a {quantidade_maxima} tópicos conforme configuração")

print("Tópicos que serão processados:")
for i, t in enumerate(topicos, 1):
    print(f" {i}. {t}")

# === GERAR TÍTULOS E ARTIGOS BASEADOS NOS TÓPICOS DA PLANILHA ===
for topico_geral in topicos:
    print(f"\n--- PROCESSANDO TÓPICO: {topico_geral} ---")

    try:
        # === GERAR TÍTULO ESPECÍFICO BASEADO NO TÓPICO GERAL ===
        prompt_titulo = f"""
Você é um especialista em criação de conteúdo para entretenimento e estilo de vida. Com base no tópico geral “{topico_geral}”, crie UM título específico e otimizado para SEO em Portugues, voltado para blog.

O título deve:
    •	Focar em tendências recentes, notícias ou acontecimentos nas áreas de: filmes, séries, livros, viagens, história ou cultura pop
    •	Basear-se em eventos atuais de fontes confiáveis como IMDb, Netflix, Amazon Prime, Disney+, grandes editoras, sites de viagem ou descobertas históricas
    •	Ser altamente pesquisável e atrativo para SEO
    •	Ter como público-alvo entusiastas do entretenimento e o público geral
    •	Ter entre 50 e 80 caracteres, ideal para SEO
    •	Incluir palavras-chave que estão em alta nas buscas

Exemplos de bons títulos:
- "As séries mais assistidas da Netflix em 2024: Guia completo de ranking"
- "10 filmes que estreiam em 2025 e que todo mundo vai comentar"
- "As histórias reais por trás de 5 documentários criminais da Netflix"

Retorne APENAS o título, nada mais.
"""

        response_titulo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um jornalista especializado em entretenimento e estrategista de conteúdo SEO, com profundo conhecimento em filmes, séries de TV, livros, viagens e tendências da cultura pop."},
                {"role": "user", "content": prompt_titulo}
            ],
            temperature=0.8,  # Mais criatividade para títulos cativantes
            max_tokens=120
        )

        titulo_especifico = response_titulo.choices[0].message.content.strip().strip('"')
        print(f"[INFO] Título gerado: {titulo_especifico}")

        # === GERAR ARTIGO BASEADO EM PESQUISA ===
        prompt_artigo = f"""
Escreva um post de blog completo e otimizado para SEO com 1000 a 1200 palavras, intitulado: "{titulo_especifico}"

 Fontes Internacionais:
    •	Filmes/Séries: IMDb, Rotten Tomatoes, Netflix, Disney+, HBO Max, Amazon Prime
    •	Livros: Goodreads, Publishers Weekly, New York Times Book Review
    •	Viagens: Lonely Planet, National Geographic, TripAdvisor, sites oficiais de turismo
    •	História: National Geographic, History Channel, Smithsonian, descobertas arqueológicas
    •	Cultura Pop: Entertainment Weekly, Variety, The Hollywood Reporter

 Fontes Brasileiras:
    •	Filmes/Séries: AdoroCinema, Omelete, Canaltech, TecMundo, Rolling Stone Brasil
    •	Livros: PublishNews, Revista Quatro Cinco Um, Estadão, Folha Ilustrada
    •	Viagens: Melhores Destinos, Viaje na Viagem, UOL Viagem, Ministério do Turismo
    •	História/Cultura: Aventuras na História, Revista Superinteressante, Brasil Escola, Globo História

ESTRUTURA DO ARTIGO E REQUISITOS DE SEO:
    1.	Introdução Atrativa (150–200 palavras):
    •	Comece com um fato envolvente, estatística ou evento recente
    •	Inclua a palavra-chave principal naturalmente no primeiro parágrafo
    •	Deixe claro o que o leitor aprenderá no artigo
    2.	Conteúdo Principal (700–800 palavras):
    •	Use subtítulos H2 e H3 com palavras-chave
    •	Divida o conteúdo em 3 ou 4 seções principais
    •	Use listas com marcadores e numeradas
    •	Adicione dados específicos, datas, nomes e estatísticas
    •	Utilize palavras-chave semânticas naturalmente ao longo do texto
    3.	Valor Prático:
    •	Ofereça dicas, recomendações ou guias acionáveis
    •	Inclua seções como “o que assistir”, “onde visitar” ou “como fazer”
    •	Crie listas comparativas ou rankings sempre que for relevante
    4.	Conclusão Envolvente (100–150 palavras):
    •	Resuma os principais pontos do artigo
    •	Inclua uma chamada para ação ou uma pergunta para engajamento
    •	Encerre com uma observação voltada para o futuro

⸻

OTIMIZAÇÃO SEO:
    •	Densidade da palavra-chave: 1–2%
    •	Inclua palavras-chave relacionadas e sinônimos
    •	Use linguagem compatível com meta descriptions
    •	Crie conteúdo que responda a perguntas comuns de busca
    •	Inclua números e superlativos nos subtítulos

⸻

TOM E ESTILO:
    •	Conversacional e informativo
    •	Entusiástico sobre o tema
    •	Acessível para o público geral
    •	Inclua personalidade e opiniões
    •	Use elementos de storytelling (narrativa)
Foco do topico: {topico_geral}

Torne o conteúdo envolvente, informativo e altamente compartilhável, mantendo as melhores práticas de SEO."""

        response_artigo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um jornalista especializado em entretenimento e estilo de vida, com amplo conhecimento em filmes, séries de TV, livros, destinos de viagem e tendências culturais. Você cria conteúdos altamente envolventes e otimizados para SEO, que têm bom desempenho no Google e mantêm os leitores engajados."},
                {"role": "user", "content": prompt_artigo}
            ],
            temperature=0.7,  # Balanceado para criatividade e precisão
            max_tokens=3000   # Mais tokens para artigos mais longos
        )

        conteudo = response_artigo.choices[0].message.content.strip()

        # === BUSCAR/CRIAR CATEGORIA CONFIGURADA ===
        categoria_desejada = config_execucao.get('categoria_wp', 'Others')
        try:
            categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
            categories_response = requests.get(categories_endpoint, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
            categories_response.raise_for_status()
            
            categories = categories_response.json()
            category_id = None
            
            # Buscar a categoria configurada
            for category in categories:
                if category['name'].lower() == categoria_desejada.lower():
                    category_id = category['id']
                    break
            
            # Se não encontrar a categoria, criar uma nova
            if category_id is None:
                create_category_data = {
                    'name': categoria_desejada,
                    'slug': categoria_desejada.lower().replace(' ', '-')
                }
                create_response = requests.post(categories_endpoint, json=create_category_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
                create_response.raise_for_status()
                category_id = create_response.json()['id']
                print(f"[INFO] Categoria '{categoria_desejada}' criada com ID: {category_id}")
            else:
                print(f"[INFO] Usando categoria existente '{categoria_desejada}' com ID: {category_id}")
            
        except Exception as e:
            print(f"[AVISO] Erro ao buscar/criar categoria '{categoria_desejada}': {e}")
            category_id = 1  # ID padrão (Uncategorized)

        # === PUBLICAR NO WORDPRESS ===
        status_publicacao = config_execucao.get('status_publicacao', 'draft')
        post_data = {
            'title': titulo_especifico,
            'content': conteudo,
            'status': status_publicacao,
            'categories': [category_id]
        }

        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        response_wp = requests.post(endpoint, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=20)
        response_wp.raise_for_status()

        status_msg = "publicado" if status_publicacao == "publish" else "salvo como rascunho"
        print(f"[✔] Post {status_msg} com sucesso na categoria '{categoria_desejada}': {titulo_especifico}")

    except Exception as e:
        print(f"[ERRO ao gerar/publicar '{titulo_especifico if 'titulo_especifico' in locals() else topico_geral}']: {e}")

    time.sleep(10)  # Evita bloqueios na API do WordPress

print("\n--- FINALIZADO COM SUCESSO ---")