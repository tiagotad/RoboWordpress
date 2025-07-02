# 1. Importar as bibliotecas necessárias
import requests
import time
import os
from openai import OpenAI
from requests.auth import HTTPBasicAuth
import gspread
from google.oauth2.service_account import Credentials

from config import *
from prompt_manager import get_prompt_titulo, get_prompt_artigo, get_system_prompts

# Validar configurações ao iniciar
if not validar_configuracoes():
    exit(1)

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
        
        # Verificar se o arquivo de credenciais existe
        if not os.path.exists(CREDENTIALS_FILE):
            raise FileNotFoundError(f"Arquivo de credenciais não encontrado: {CREDENTIALS_FILE}")
        
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

print("Tópicos que serão processados:")
for i, t in enumerate(topicos, 1):
    print(f" {i}. {t}")

# === GERAR TÍTULOS E ARTIGOS BASEADOS NOS TÓPICOS DA PLANILHA ===
for topico_geral in topicos:
    print(f"\n--- PROCESSANDO TÓPICO: {topico_geral} ---")

    try:
        # === GERAR TÍTULO ESPECÍFICO BASEADO NO TÓPICO GERAL ===
        print("[INFO] Carregando prompt personalizado para título...")
        prompt_titulo = get_prompt_titulo(topico_geral)
        system_prompts = get_system_prompts()

        response_titulo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompts['titulo']},
                {"role": "user", "content": prompt_titulo}
            ],
            temperature=0.8,  # Mais criatividade para títulos cativantes
            max_tokens=120
        )

        titulo_especifico = response_titulo.choices[0].message.content.strip().strip('"')
        print(f"[INFO] Título gerado: {titulo_especifico}")

        # === GERAR ARTIGO BASEADO EM PESQUISA ===
        print("[INFO] Carregando prompt personalizado para artigo...")
        prompt_artigo = get_prompt_artigo(titulo_especifico, topico_geral)

        response_artigo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompts['artigo']},
                {"role": "user", "content": prompt_artigo}
            ],
            temperature=0.7,  # Balanceado para criatividade e precisão
            max_tokens=3000   # Mais tokens para artigos mais longos
        )

        conteudo = response_artigo.choices[0].message.content.strip()

        # === BUSCAR ID DA CATEGORIA "Others" ===
        try:
            categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
            categories_response = requests.get(categories_endpoint, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
            categories_response.raise_for_status()
            
            categories = categories_response.json()
            others_category_id = None
            
            # Buscar a categoria "Others"
            for category in categories:
                if category['name'].lower() == 'others':
                    others_category_id = category['id']
                    break
            
            # Se não encontrar a categoria "Others", criar uma nova
            if others_category_id is None:
                create_category_data = {
                    'name': 'Others',
                    'slug': 'others'
                }
                create_response = requests.post(categories_endpoint, json=create_category_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
                create_response.raise_for_status()
                others_category_id = create_response.json()['id']
                print(f"[INFO] Categoria 'Others' criada com ID: {others_category_id}")
            
        except Exception as e:
            print(f"[AVISO] Erro ao buscar/criar categoria 'Others': {e}")
            others_category_id = 1  # ID padrão (Uncategorized)

        # === PUBLICAR NO WORDPRESS COMO RASCUNHO ===
        post_data = {
            'title': titulo_especifico,
            'content': conteudo,
            'status': 'draft',  # Salva como rascunho para revisão
            'categories': [others_category_id]  # Adiciona à categoria Others
        }

        endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        response_wp = requests.post(endpoint, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=20)
        response_wp.raise_for_status()

        print(f"[✔] Rascunho salvo com sucesso na categoria 'Others': {titulo_especifico}")
        print(f"[INFO] Usando prompts personalizados do arquivo prompts.json")

    except Exception as e:
        print(f"[ERRO ao gerar/publicar '{titulo_especifico if 'titulo_especifico' in locals() else topico_geral}']: {e}")

    time.sleep(10)  # Evita bloqueios na API do WordPress

print("\n--- FINALIZADO COM SUCESSO ---")
print("[INFO] 🎯 Para editar os prompts, use a interface web: streamlit run app.py")
