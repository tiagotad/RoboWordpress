import streamlit as st
import time
import os
import json
import requests
from datetime import datetime

# Detectar ambiente cloud
def detect_streamlit_cloud():
    if os.getenv('STREAMLIT_CLOUD', '').lower() == 'true':
        return 'envvar'
    if hasattr(st, 'secrets') and hasattr(st.secrets, '_secrets_file'):
        if getattr(st.secrets, '_secrets_file', 'notfound') is None:
            return 'secretsfile'
    if hasattr(st, 'secrets') and 'WP_URL' in st.secrets and not os.path.exists('config.py'):
        return 'heuristic'
    return ''

is_streamlit_cloud_mode = detect_streamlit_cloud()
is_streamlit_cloud = bool(is_streamlit_cloud_mode)

# Configurar página
st.set_page_config(
    page_title="RoboWordpress - Gerador de Conteúdo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para interface limpa
st.markdown("""
<style>
    .main {
        padding: 1rem 2rem;
    }
    
    .sidebar .sidebar-content {
        padding: 1rem;
    }
    
    .status-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    .status-error {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    .status-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 4px;
    }
    
    .log-container {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
        height: 400px;
        overflow-y: auto;
    }
    
    .test-section {
        background-color: #f1f3f4;
        padding: 0.5rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
    
    .compact-input {
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Carregar configurações
try:
    if is_streamlit_cloud:
        from config_cloud import *
    else:
        from config import *
except ImportError as e:
    st.error(f"Erro ao carregar configurações: {e}")
    st.stop()

# Funções auxiliares
def test_wordpress_connection():
    """Testa conexão com WordPress"""
    try:
        url = f"{WP_URL}/wp-json/wp/v2/users/me"
        response = requests.get(url, auth=(WP_USER, WP_PASSWORD), timeout=10)
        if response.status_code == 200:
            return True, "✅ WordPress conectado"
        else:
            return False, f"❌ Erro {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"❌ Erro de conexão: {str(e)}"

def get_wordpress_authors():
    """Busca lista de autores do WordPress"""
    try:
        url = f"{WP_URL}/wp-json/wp/v2/users"
        response = requests.get(url, auth=(WP_USER, WP_PASSWORD), timeout=10)
        if response.status_code == 200:
            users = response.json()
            authors = []
            for user in users:
                # Incluir todos os usuários que podem criar posts
                capabilities = user.get('capabilities', {})
                if (isinstance(capabilities, dict) and 
                    (capabilities.get('edit_posts', False) or 
                     capabilities.get('publish_posts', False) or
                     'author' in str(capabilities).lower())):
                    authors.append({
                        'id': user['id'],
                        'name': user['name'],
                        'slug': user['slug']
                    })
                # Fallback: se não tem capabilities, incluir mesmo assim
                elif not capabilities:
                    authors.append({
                        'id': user['id'],
                        'name': user['name'],
                        'slug': user['slug']
                    })
            
            # Se não encontrou nenhum autor, criar lista com usuários básicos
            if not authors:
                for user in users:
                    authors.append({
                        'id': user['id'],
                        'name': user['name'],
                        'slug': user['slug']
                    })
            
            return True, authors
        else:
            return False, f"Erro {response.status_code}: {response.text}"
    except Exception as e:
        return False, f"Erro de conexão: {str(e)}"

def create_execution_config(categoria, status, quantidade, topicos, author_id):
    """Cria arquivo de configuração de execução"""
    config_data = {
        'categoria_wp': categoria,
        'status_publicacao': status,
        'quantidade_textos': quantidade,
        'topicos_lista': topicos,
        'author_id': author_id
    }
    
    config_content = f'''# Configurações de Execução - Gerado automaticamente
# {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

def get_configuracoes_execucao():
    return {json.dumps(config_data, indent=4, ensure_ascii=False)}
'''
    
    try:
        with open('config_execucao.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        return True, "Configuração salva com sucesso"
    except Exception as e:
        return False, f"Erro ao salvar: {str(e)}"

def load_prompts():
    """Carrega prompts do arquivo prompts.json"""
    try:
        if os.path.exists('prompts.json'):
            with open('prompts.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Prompts padrão
            return {
                "system_prompts": {
                    "titulo": "Você é um especialista em criar títulos cativantes para blogs. Crie títulos que sejam informativos, envolventes e otimizados para SEO.",
                    "artigo": "Você é um escritor experiente que cria artigos informativos e envolventes. Escreva sempre em português brasileiro com linguagem clara e profissional."
                },
                "prompt_titulo": "Crie um título atrativo e informativo sobre: {topico}. O título deve ter entre 40-60 caracteres e ser otimizado para SEO.",
                "prompt_artigo": "Escreva um artigo completo e informativo sobre '{titulo}' relacionado ao tema '{topico}'. O artigo deve ter pelo menos 800 palavras, com introdução, desenvolvimento e conclusão."
            }
    except Exception as e:
        st.error(f"Erro ao carregar prompts: {e}")
        return {}

def save_prompts(prompts_data):
    """Salva prompts no arquivo prompts.json"""
    try:
        with open('prompts.json', 'w', encoding='utf-8') as f:
            json.dump(prompts_data, f, indent=4, ensure_ascii=False)
        return True, "Prompts salvos com sucesso!"
    except Exception as e:
        return False, f"Erro ao salvar prompts: {e}"

def generate_preview_content(titulo_prompt, artigo_prompt, topico_exemplo="Tecnologia"):
    """Gera preview do conteúdo usando os prompts personalizados"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Gerar título
        response_titulo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um especialista em criar títulos cativantes."},
                {"role": "user", "content": titulo_prompt.format(topico=topico_exemplo)}
            ],
            max_tokens=100,
            temperature=0.7
        )
        titulo_gerado = response_titulo.choices[0].message.content.strip()
        
        # Gerar preview do artigo (apenas início)
        response_artigo = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um escritor experiente."},
                {"role": "user", "content": artigo_prompt.format(titulo=titulo_gerado, topico=topico_exemplo)[:200] + "... (apenas os primeiros 200 caracteres para preview)"}
            ],
            max_tokens=200,
            temperature=0.7
        )
        artigo_preview = response_artigo.choices[0].message.content.strip()
        
        return True, titulo_gerado, artigo_preview
    except Exception as e:
        return False, f"Erro ao gerar preview: {e}", ""

# SIDEBAR - Área de Testes
with st.sidebar:
    st.header("🔧 Testes")
    
    # Teste WordPress
    with st.expander("WordPress API", expanded=False):
        if st.button("Testar Conexão", key="test_wp", use_container_width=True):
            with st.spinner("Testando..."):
                success, message = test_wordpress_connection()
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    # Teste OpenAI
    with st.expander("OpenAI API", expanded=False):
        if st.button("Testar API", key="test_openai", use_container_width=True):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": "Teste"}],
                    max_tokens=10
                )
                st.success("✅ OpenAI conectado")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
    
    st.divider()
    st.caption("ℹ️ Use os testes para verificar se as APIs estão funcionando.")

# ÁREA PRINCIPAL
st.title("🤖 RoboWordpress - Gerador de Conteúdo")
st.markdown("**Gere posts automaticamente para seu WordPress com IA**")

# Criar abas para organizar melhor
tab_config, tab_prompts, tab_preview = st.tabs(["⚙️ Configuração", "🎨 Personalizar IA", "👁️ Preview"])

with tab_config:
    # Criar colunas para layout
    col1, col2 = st.columns([2, 1])

    with col1:
        # Seção de Configuração
        st.header("⚙️ Configuração Básica")
        
        # Buscar autores
        authors_success, authors_data = get_wordpress_authors()
        
        # Debug: mostrar informações dos autores
        if authors_success:
            st.success(f"✅ {len(authors_data)} autores encontrados")
            with st.expander("🔍 Debug - Autores encontrados"):
                st.json(authors_data)
        else:
            st.error(f"❌ Erro ao buscar autores: {authors_data}")
        
        with st.form("config_form"):
            st.subheader("Configurações Básicas")
            
            # Autor
            if authors_success and authors_data:
                author_options = {f"{author['name']} (ID: {author['id']})": author['id'] for author in authors_data}
                
                # Tentar definir "mateus" como padrão
                default_author_idx = 0
                for idx, (display_name, author_id) in enumerate(author_options.items()):
                    if 'mateus' in display_name.lower():
                        default_author_idx = idx
                        break
                
                selected_author_display = st.selectbox(
                    "👤 Autor do Post",
                    options=list(author_options.keys()),
                    index=default_author_idx,
                    help="Selecione o autor que será creditado nos posts"
                )
            else:
                st.error(f"❌ Erro ao carregar autores: {authors_data}")
                selected_author_display = "mateus (ID: 18) - Padrão"
                author_options = {selected_author_display: 18}
            
            # Categoria e Status
            col_cat, col_status = st.columns(2)
            with col_cat:
                categoria = st.text_input("📁 Categoria", value="Others", help="Nome da categoria no WordPress")
            with col_status:
                status = st.selectbox("📝 Status", ["draft", "publish"], help="Status do post após criação")
            
            # Quantidade de textos
            quantidade_textos = st.slider(
                "📊 Quantidade de textos por tópico",
                min_value=1,
                max_value=20,
                value=3,
                help="Quantos textos serão gerados para cada tópico"
            )
            
            st.subheader("Tópicos")
            
            # Input de tópicos
            topicos_input = st.text_area(
                "📝 Lista de Tópicos (um por linha)",
                value="Tecnologia\nSaúde e Bem-estar\nViagens e Turismo",
                height=120,
                help="Digite um tópico por linha. Exemplo:\nTecnologia\nSaúde\nViagens"
            )
            
            # Processar tópicos
            topicos = [t.strip() for t in topicos_input.split('\n') if t.strip()]
            
            if topicos:
                st.info(f"📋 **{len(topicos)} tópicos** → **{len(topicos) * quantidade_textos} posts totais**")
                
                # Mostrar resumo
                with st.expander("Ver detalhes dos tópicos"):
                    for i, topico in enumerate(topicos, 1):
                        st.write(f"{i}. **{topico}** ({quantidade_textos} textos)")
            
            # Botão de execução
            submitted = st.form_submit_button("🚀 Salvar Configuração", use_container_width=True, type="primary")
            
            if submitted:
                # Obter ID do autor selecionado
                selected_author_id = author_options[selected_author_display]
                
                if not topicos:
                    st.error("❌ Por favor, adicione pelo menos um tópico!")
                else:
                    # Salvar configuração
                    success, message = create_execution_config(
                        categoria, status, quantidade_textos, topicos, selected_author_id
                    )
                    
                    if success:
                        st.success(f"✅ {message}")
                        st.info(f"👤 **Autor selecionado:** {selected_author_display}")
                        st.info(f"📊 **Configuração:** {quantidade_textos} textos × {len(topicos)} tópicos = {len(topicos) * quantidade_textos} posts")
                        
                        # Armazenar na sessão para logs
                        st.session_state['config_saved'] = True
                        st.session_state['total_posts'] = len(topicos) * quantidade_textos
                        st.session_state['topicos'] = topicos
                        st.session_state['quantidade_textos'] = quantidade_textos
                    else:
                        st.error(f"❌ {message}")

    with col2:
        # Seção de Execução e Logs
        st.header("🔄 Execução")
        
        # Botões de execução
        if st.session_state.get('config_saved', False):
            st.success("✅ Configuração salva!")
            
            st.markdown("**Execute os robôs:**")
            
            if st.button("🔥 Executar Robô V3", use_container_width=True, type="primary"):
                st.info("🚀 Para executar o Robô V3:")
                st.code("python robo_pilloto_v3.py", language="bash")
                st.warning("⚠️ Execute este comando no terminal")
            
            if st.button("🔥 Executar Robô V4", use_container_width=True, type="primary"):
                st.info("🚀 Para executar o Robô V4:")
                st.code("python robo_pilloto_v4.py", language="bash")
                st.warning("⚠️ Execute este comando no terminal")
        else:
            st.info("ℹ️ Configure e salve primeiro")
        
        # Área de Status
        st.subheader("📊 Status")
        if st.session_state.get('config_saved', False):
            total = st.session_state.get('total_posts', 0)
            st.metric("Posts a gerar", total)
            st.metric("Tópicos", len(st.session_state.get('topicos', [])))
            st.metric("Textos por tópico", st.session_state.get('quantidade_textos', 0))
        else:
            st.text("Aguardando configuração...")

with tab_prompts:
    st.header("🎨 Personalizar Personalidade da IA")
    st.markdown("**Configure como a IA irá gerar títulos e conteúdo**")
    
    # Carregar prompts existentes
    current_prompts = load_prompts()
    
    with st.form("prompts_form"):
        col_prompts1, col_prompts2 = st.columns(2)
        
        with col_prompts1:
            st.subheader("🧠 Personalidade para Títulos")
            system_titulo = st.text_area(
                "Como a IA deve se comportar ao criar títulos:",
                value=current_prompts.get('system_prompts', {}).get('titulo', ''),
                height=120,
                help="Defina a personalidade da IA para criação de títulos"
            )
            
            prompt_titulo = st.text_area(
                "Template do prompt para títulos:",
                value=current_prompts.get('prompt_titulo', ''),
                height=100,
                help="Use {topico} onde quiser inserir o tópico"
            )
        
        with col_prompts2:
            st.subheader("✍️ Personalidade para Artigos")
            system_artigo = st.text_area(
                "Como a IA deve se comportar ao escrever artigos:",
                value=current_prompts.get('system_prompts', {}).get('artigo', ''),
                height=120,
                help="Defina a personalidade da IA para escrita de artigos"
            )
            
            prompt_artigo = st.text_area(
                "Template do prompt para artigos:",
                value=current_prompts.get('prompt_artigo', ''),
                height=100,
                help="Use {titulo} e {topico} onde necessário"
            )
        
        # Botão para salvar prompts
        if st.form_submit_button("💾 Salvar Personalização", use_container_width=True, type="primary"):
            new_prompts = {
                "system_prompts": {
                    "titulo": system_titulo,
                    "artigo": system_artigo
                },
                "prompt_titulo": prompt_titulo,
                "prompt_artigo": prompt_artigo
            }
            
            success, message = save_prompts(new_prompts)
            if success:
                st.success(f"✅ {message}")
                st.rerun()
            else:
                st.error(f"❌ {message}")

with tab_preview:
    st.header("👁️ Preview do Conteúdo")
    st.markdown("**Veja como a IA gerará o conteúdo com suas configurações**")
    
    # Carregar prompts atuais
    current_prompts = load_prompts()
    
    col_prev1, col_prev2 = st.columns([1, 1])
    
    with col_prev1:
        st.subheader("🎯 Configurar Preview")
        
        topico_teste = st.text_input(
            "Tópico para teste:",
            value="Inteligência Artificial",
            help="Digite um tópico para ver como a IA gerará o conteúdo"
        )
        
        if st.button("🚀 Gerar Preview", type="primary"):
            if current_prompts and topico_teste:
                with st.spinner("Gerando preview..."):
                    success, titulo, artigo_preview = generate_preview_content(
                        current_prompts.get('prompt_titulo', ''),
                        current_prompts.get('prompt_artigo', ''),
                        topico_teste
                    )
                    
                    if success:
                        st.session_state['preview_titulo'] = titulo
                        st.session_state['preview_artigo'] = artigo_preview
                        st.success("✅ Preview gerado!")
                        st.rerun()
                    else:
                        st.error(f"❌ {titulo}")  # titulo contém erro se success=False
            else:
                st.warning("⚠️ Configure os prompts primeiro na aba 'Personalizar IA'")
    
    with col_prev2:
        st.subheader("📝 Resultado do Preview")
        
        if 'preview_titulo' in st.session_state:
            st.markdown("**🏷️ Título Gerado:**")
            st.info(st.session_state['preview_titulo'])
            
            st.markdown("**📄 Preview do Artigo:**")
            st.text_area(
                "Conteúdo:",
                value=st.session_state['preview_artigo'],
                height=200,
                disabled=True
            )
        else:
            st.info("👆 Clique em 'Gerar Preview' para ver o resultado")

# Rodapé
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <small>🤖 RoboWordpress | Geração automática de conteúdo com IA</small>
</div>
""", unsafe_allow_html=True)
