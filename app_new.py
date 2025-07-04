import streamlit as st
import pandas as pd
import time
import sys
import os
from datetime import datetime
import subprocess
import threading
from io import StringIO
import json
import requests
import queue

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
                if 'author' in user.get('capabilities', {}) or user.get('capabilities', {}).get('edit_posts', False):
                    authors.append({
                        'id': user['id'],
                        'name': user['name'],
                        'slug': user['slug']
                    })
            return True, authors
        else:
            return False, f"Erro {response.status_code}"
    except Exception as e:
        return False, str(e)

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

# Criar colunas para layout
col1, col2 = st.columns([2, 1])

with col1:
    # Seção de Configuração
    st.header("⚙️ Configuração")
    
    # Buscar autores
    authors_success, authors_data = get_wordpress_authors()
    
    with st.form("config_form"):
        st.subheader("Configurações Básicas")
        
        # Autor
        if authors_success:
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
            selected_author_id = author_options[selected_author_display]
        else:
            st.error(f"❌ Erro ao carregar autores: {authors_data}")
            selected_author_id = 18  # Fallback
            selected_author_display = "mateus (ID: 18) - Padrão"
        
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
        submitted = st.form_submit_button("🚀 Gerar Conteúdo", use_container_width=True, type="primary")
        
        if submitted:
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
        
        col_v3, col_v4 = st.columns(2)
        
        with col_v3:
            if st.button("▶️ Robô V3", use_container_width=True):
                st.session_state['executing'] = 'v3'
                st.rerun()
        
        with col_v4:
            if st.button("▶️ Robô V4", use_container_width=True):
                st.session_state['executing'] = 'v4'
                st.rerun()
    else:
        st.info("ℹ️ Configure e salve primeiro")
    
    # Área de Logs em Tempo Real
    st.subheader("📋 Logs em Tempo Real")
    
    # Container para logs
    log_container = st.empty()
    
    # Se estiver executando
    if st.session_state.get('executing'):
        robot_version = st.session_state['executing']
        script_name = f"robo_pilloto_v{robot_version}.py"
        
        st.info(f"🤖 Executando {script_name}...")
        
        # Criar processo
        try:
            process = subprocess.Popen(
                [sys.executable, script_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Container para logs dinâmicos
            logs = []
            placeholder = st.empty()
            
            # Ler output em tempo real
            for line in process.stdout:
                logs.append(line.strip())
                
                # Limitar logs (últimas 50 linhas)
                if len(logs) > 50:
                    logs = logs[-50:]
                
                # Atualizar display
                log_text = '\n'.join(logs)
                placeholder.text_area(
                    "Logs:",
                    value=log_text,
                    height=400,
                    disabled=True,
                    key=f"logs_{time.time()}"
                )
                
                time.sleep(0.1)  # Pequena pausa para não sobrecarregar
            
            # Finalizar
            process.wait()
            
            if process.returncode == 0:
                st.success("✅ Execução concluída com sucesso!")
            else:
                st.error("❌ Execução finalizada com erros")
            
            # Limpar estado
            st.session_state['executing'] = None
            
        except Exception as e:
            st.error(f"❌ Erro na execução: {str(e)}")
            st.session_state['executing'] = None
    
    else:
        # Logs estáticos quando não está executando
        with log_container.container():
            st.text_area(
                "Logs:",
                value="Aguardando execução...\nSelecione um robô para começar.",
                height=400,
                disabled=True
            )

# Rodapé
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <small>🤖 RoboWordpress | Geração automática de conteúdo com IA</small>
</div>
""", unsafe_allow_html=True)
