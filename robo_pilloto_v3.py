#!/usr/bin/env python3
"""
RoboWordpress v3 - Gerador de Conteúdo Automatizado
Sistema simplificado com prompt único
"""

import sys
import requests
import time
from datetime import datetime
from openai import OpenAI
from requests.auth import HTTPBasicAuth

def log(message):
    """Log com timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

# Importar configurações com fallback para Streamlit Cloud
try:
    # Tentar importar config local primeiro
    from config import *
    log("✅ Configurações locais carregadas")
except ImportError:
    # Se falhar, tentar config_cloud
    try:
        from config_cloud import *
        log("🌐 Usando configurações do Streamlit Cloud")
    except ImportError:
        # Se ambos falharem, usar configurações diretas do Streamlit
        try:
            import streamlit as st
            log("🌐 Usando configurações diretas do Streamlit")
            
            # Configurações do WordPress
            WP_URL = st.secrets["WP_URL"]
            WP_USER = st.secrets["WP_USER"]
            WP_PASSWORD = st.secrets["WP_PASSWORD"]
            
            # Configurações da OpenAI
            OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
            
            # Configurações do Google Sheets
            GOOGLE_SHEET_ID = st.secrets.get("GOOGLE_SHEET_ID", "")
            CREDENTIALS_FILE = st.secrets.get("CREDENTIALS_FILE", "credenciais_google.json")
            
            log("✅ Configurações do Streamlit carregadas")
            
        except Exception as e:
            log(f"❌ Erro ao carregar configurações: {e}")
            log("💡 Configure as variáveis no Streamlit Secrets ou arquivo .env local")
            sys.exit(1)

try:
    from config_execucao import get_configuracoes_execucao
    from prompt_manager import get_prompt_completo, get_system_prompt
    
    # Configurações
    client = OpenAI(api_key=OPENAI_API_KEY)
    config = get_configuracoes_execucao()
    
except ImportError as e:
    log(f"❌ Erro ao importar módulos: {e}")
    sys.exit(1)
except Exception as e:
    log(f"❌ Erro ao inicializar: {e}")
    sys.exit(1)

def gerar_conteudo(topico):
    """Gera título e artigo usando prompt único"""
    log(f"Gerando conteúdo para: {topico}")
    
    prompt = get_prompt_completo(topico)
    system_prompt = get_system_prompt()
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=4000
    )
    
    resposta = response.choices[0].message.content.strip()
    
    # Extrair título e artigo
    if "TÍTULO:" in resposta:
        partes = resposta.split("TÍTULO:", 1)[1].split("ARTIGO:", 1)
        titulo = partes[0].strip()
        artigo = partes[1].strip() if len(partes) > 1 else ""
    else:
        linhas = resposta.split("\n", 1)
        titulo = linhas[0].strip()
        artigo = linhas[1].strip() if len(linhas) > 1 else resposta
    
    return titulo, artigo

def gerar_tags(titulo, artigo, topico):
    """Gera tags relevantes baseadas no conteúdo"""
    log("Gerando tags para o artigo...")
    
    prompt_tags = f"""
    Baseado no título, artigo e tópico abaixo, gere 5-8 tags relevantes para WordPress.
    As tags devem ser:
    - Palavras-chave importantes do conteúdo
    - Termos que pessoas buscariam no Google
    - Relacionadas ao tópico principal
    - Em português
    
    TÍTULO: {titulo}
    TÓPICO: {topico}
    ARTIGO: {artigo[:500]}...
    
    Responda APENAS com as tags separadas por vírgula, sem numeração ou formatação extra.
    Exemplo: tecnologia, inteligência artificial, inovação, futuro, automação
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um especialista em SEO e criação de tags para WordPress. Gere tags relevantes e otimizadas."},
            {"role": "user", "content": prompt_tags}
        ],
        temperature=0.3,
        max_tokens=200
    )
    
    tags_text = response.choices[0].message.content.strip()
    tags = [tag.strip() for tag in tags_text.split(',') if tag.strip()]
    
    log(f"Tags geradas: {', '.join(tags)}")
    return tags

def criar_tags_wordpress(tags):
    """Cria tags no WordPress e retorna seus IDs"""
    tag_ids = []
    
    for tag_name in tags:
        try:
            # Verificar se a tag já existe
            tags_response = requests.get(
                f"{WP_URL}/wp-json/wp/v2/tags",
                params={'search': tag_name},
                auth=HTTPBasicAuth(WP_USER, WP_PASSWORD),
                timeout=10
            )
            
            existing_tags = tags_response.json()
            
            # Se a tag existe, usar o ID existente
            if existing_tags:
                tag_id = existing_tags[0]['id']
                log(f"Tag existente: '{tag_name}' (ID: {tag_id})")
            else:
                # Criar nova tag
                create_response = requests.post(
                    f"{WP_URL}/wp-json/wp/v2/tags",
                    json={'name': tag_name},
                    auth=HTTPBasicAuth(WP_USER, WP_PASSWORD),
                    timeout=10
                )
                create_response.raise_for_status()
                tag_id = create_response.json()['id']
                log(f"Nova tag criada: '{tag_name}' (ID: {tag_id})")
            
            tag_ids.append(tag_id)
            
        except Exception as e:
            log(f"⚠️ Erro ao processar tag '{tag_name}': {e}")
            continue
    
    return tag_ids

def publicar_post(titulo, conteudo, tags):
    """Publica post no WordPress com tags"""
    log(f"📤 Publicando post: {titulo}")
    
    # Criar tags no WordPress
    tag_ids = criar_tags_wordpress(tags)
    
    post_data = {
        'title': titulo,
        'content': conteudo,
        'status': config.get('status_publicacao', 'draft'),
        'categories': [config.get('categoria_wp', 32174)],
        'tags': tag_ids,
        'author': config.get('author_id', 1)
    }
    
    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        json=post_data,
        auth=HTTPBasicAuth(WP_USER, WP_PASSWORD),
        timeout=20
    )
    response.raise_for_status()
    
    post_response = response.json()
    post_id = post_response['id']
    post_url = post_response.get('link', f"{WP_URL}/?p={post_id}")
    
    status_publicacao = config.get('status_publicacao', 'draft')
    status_msg = "publicado" if status_publicacao == "publish" else "salvo como rascunho"
    
    log(f"✅ Post {status_msg} com sucesso!")
    log(f"📌 ID: {post_id} | Tags: {len(tag_ids)} | Categoria: {config.get('categoria_wp', 32174)}")
    log(f"🔗 URL: {post_url}")
    
    return post_id

def main():
    """Função principal"""
    log("🚀 Iniciando RoboWordpress v3")
    
    topicos = config.get('topicos_lista', [])
    if not topicos:
        log("❌ Nenhum tópico encontrado!")
        return
    
    log(f"📝 Processando {len(topicos)} tópicos")
    
    posts_criados = 0
    posts_falharam = 0
    
    for i, topico in enumerate(topicos, 1):
        try:
            log(f"--- TÓPICO {i}/{len(topicos)}: {topico} ---")
            
            titulo, artigo = gerar_conteudo(topico)
            tags = gerar_tags(titulo, artigo, topico)
            post_id = publicar_post(titulo, artigo, tags)
            posts_criados += 1
            
            log(f"✅ Post #{posts_criados} criado com sucesso! ID: {post_id}")
            log(f"📊 Progresso: {posts_criados}/{len(topicos)} posts criados")
            
            time.sleep(5)  # Pausa entre posts
            
        except Exception as e:
            log(f"❌ Erro no tópico '{topico}': {e}")
            posts_falharam += 1
            continue
    
    # Estatísticas finais
    log("=" * 50)
    log("📊 ESTATÍSTICAS FINAIS:")
    log(f"✅ Posts criados com sucesso: {posts_criados}")
    log(f"❌ Posts que falharam: {posts_falharam}")
    log(f"📝 Total de tópicos processados: {len(topicos)}")
    log(f"� Taxa de sucesso: {(posts_criados/len(topicos)*100):.1f}%")
    log("=" * 50)
    
    if posts_criados > 0:
        log(f"�🎉 Execução concluída! {posts_criados} posts foram criados com sucesso!")
    else:
        log("⚠️ Nenhum post foi criado. Verifique os logs de erro acima.")

if __name__ == "__main__":
    main()
