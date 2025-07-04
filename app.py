
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
    page_title="RoboWordpress - Painel de Controle",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .status-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .status-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .status-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .robot-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Versão do app
APP_VERSION = "2.0.0 - Interface de Tópicos Integrada 2025-07-02"

# Função para validar credenciais WordPress
def validar_credenciais_wordpress(wp_url, wp_user, wp_password):
    """Valida as credenciais do WordPress testando a conexão com a API"""
    try:
        import requests
        from requests.auth import HTTPBasicAuth
        
        # Garantir que a URL termina sem barra
        wp_url = wp_url.rstrip('/')
        
        # Teste de autenticação
        response = requests.get(
            f'{wp_url}/wp-json/wp/v2/users/me',
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return True, f"Conectado como: {user_data.get('name', 'N/A')}"
        elif response.status_code == 401:
            return False, "Falha na autenticação! Verifique usuário e senha."
        else:
            return False, f"Erro na conexão: {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Timeout: O site demorou para responder"
    except requests.exceptions.ConnectionError:
        return False, "Erro de conexão: Verifique se a URL está correta"
    except Exception as e:
        return False, f"Erro: {str(e)}"

# Modal de Login Obrigatório
if 'wp_authenticated' not in st.session_state:
    st.session_state.wp_authenticated = False
    st.session_state.wp_url = ""
    st.session_state.wp_user = ""
    st.session_state.wp_password = ""
    st.session_state.wp_user_info = ""

# Se não estiver autenticado, mostrar apenas o modal de login
if not st.session_state.wp_authenticated:
    st.markdown(f'<h1 class="main-header">🔐 RoboWordpress - Login Obrigatório</h1>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    ## 🚨 **Acesso Restrito**
    
    **Para usar o RoboWordpress, você deve fornecer credenciais válidas do WordPress.**
    
    ⚡ **Após o login bem-sucedido:**
    - ✅ Carregamento automático de autores e categorias
    - ✅ Configurações dinâmicas baseadas no seu site
    - ✅ Execução segura dos robôs com suas credenciais
    """)
    
    with st.container():
        st.markdown("### 🔑 **Credenciais do WordPress**")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            wp_url_input = st.text_input(
                "🌐 URL do WordPress:",
                value="https://www.elhombre.com.br",
                placeholder="https://seu-site-wordpress.com",
                help="URL completa do seu site WordPress (sem barra no final)"
            )
            
            wp_user_input = st.text_input(
                "👤 Usuário:",
                placeholder="seu_usuario",
                help="Nome de usuário do WordPress (Admin/Editor recomendado)"
            )
        
        with col2:
            wp_password_input = st.text_input(
                "🔑 Senha:",
                type="password",
                placeholder="sua_senha_ou_application_password",
                help="Senha do usuário ou Application Password (recomendado para 2FA)"
            )
            
            st.markdown("### 📋 **Sobre Application Passwords:**")
            st.info("""
            💡 **Recomendado:** Use Application Passwords se tiver 2FA ativo
            
            **Como criar:**
            1. WordPress Admin → Usuários → Seu Perfil
            2. Role até "Application Passwords"
            3. Digite um nome (ex: "RoboWordpress")
            4. Clique "Add New Application Password"
            5. Copie a senha gerada (formato: xxxx xxxx xxxx)
            """)
        
        st.markdown("---")
        
        col_login, col_help = st.columns([1, 2])
        
        with col_login:
            if st.button("🔐 **FAZER LOGIN**", type="primary", use_container_width=True):
                if not wp_url_input or not wp_user_input or not wp_password_input:
                    st.error("❌ **Todos os campos são obrigatórios!**")
                else:
                    with st.spinner("🔍 Validando credenciais..."):
                        sucesso, mensagem = validar_credenciais_wordpress(wp_url_input, wp_user_input, wp_password_input)
                        
                        if sucesso:
                            # Salvar credenciais na sessão
                            st.session_state.wp_authenticated = True
                            st.session_state.wp_url = wp_url_input.rstrip('/')
                            st.session_state.wp_user = wp_user_input
                            st.session_state.wp_password = wp_password_input
                            st.session_state.wp_user_info = mensagem
                            
                            st.success(f"✅ **Login bem-sucedido!** {mensagem}")
                            st.success("🔄 **Recarregando aplicação com suas credenciais...**")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(f"❌ **Falha no login:** {mensagem}")
        
        with col_help:
            with st.expander("🆘 **Problemas para fazer login?**"):
                st.markdown("""
                ### 🔧 **Soluções Comuns:**
                
                **❌ Erro 401 (Não autorizado):**
                - Verifique usuário e senha
                - Use Application Password se tiver 2FA
                
                **❌ Timeout/Conexão:**
                - Verifique se a URL está correta
                - Teste: `https://seu-site.com/wp-admin`
                
                **❌ Erro 403 (Proibido):**
                - Usuário precisa ser Admin ou Editor
                - Verifique permissões da API REST
                
                **✅ Teste manual:**
                - Acesse: `sua-url.com/wp-json/wp/v2`
                - Deve mostrar informações da API
                """)
    
    st.stop()  # Para a execução aqui até o login ser feito

# Se chegou aqui, está autenticado - continuar com a aplicação normal
st.markdown(f'<h1 class="main-header">🤖 RoboWordpress - Painel de Controle <span style="font-size:1.2rem;color:#888;">v{APP_VERSION}</span></h1>', unsafe_allow_html=True)

# Mostrar info de usuário logado
st.markdown(f"""
<div style="background-color: #d4edda; padding: 1rem; border-radius: 10px; margin-bottom: 2rem; border-left: 4px solid #28a745;">
    <h4 style="margin: 0; color: #155724;">✅ Conectado com sucesso!</h4>
    <p style="margin: 0.5rem 0 0 0; color: #155724;">
        <strong>Site:</strong> {st.session_state.wp_url} | 
        <strong>Status:</strong> {st.session_state.wp_user_info}
    </p>
</div>
""", unsafe_allow_html=True)

# Botão de logout
col_logout, col_space = st.columns([1, 4])
with col_logout:
    if st.button("🚪 Sair", help="Fazer logout e limpar credenciais"):
        st.session_state.wp_authenticated = False
        st.session_state.wp_url = ""
        st.session_state.wp_user = ""
        st.session_state.wp_password = ""
        st.session_state.wp_user_info = ""
        st.success("👋 Logout realizado!")
        time.sleep(1)
        st.rerun()

st.markdown("---")


# Verificar se está rodando no Streamlit Cloud (método robusto)

# Detecção robusta do ambiente Streamlit Cloud
def detect_streamlit_cloud():
    # 1. Variável de ambiente padrão do Streamlit Cloud
    if os.getenv('STREAMLIT_CLOUD', '').lower() == 'true':
        return 'envvar'
    # 2. st.secrets._secrets_file é None apenas no cloud
    if hasattr(st, 'secrets') and hasattr(st.secrets, '_secrets_file'):
        if getattr(st.secrets, '_secrets_file', 'notfound') is None:
            return 'secretsfile'
    # 3. Heurística: st.secrets existe e tem WP_URL, mas não existe config.py
    if hasattr(st, 'secrets') and 'WP_URL' in st.secrets and not os.path.exists('config.py'):
        return 'heuristic'
    return ''

is_streamlit_cloud_mode = detect_streamlit_cloud()
is_streamlit_cloud = bool(is_streamlit_cloud_mode)

if is_streamlit_cloud:
    st.markdown("## 🌐 **RODANDO NO STREAMLIT CLOUD**")
    
    # Verificar se secrets estão configuradas
    missing_secrets = []
    try:
        required_secrets = ['WP_URL', 'WP_USER', 'WP_PASSWORD', 'OPENAI_API_KEY']
        for secret in required_secrets:
            if secret not in st.secrets or not st.secrets.get(secret):
                missing_secrets.append(secret)
    except Exception:
        missing_secrets = ['Todas as credenciais']

    if missing_secrets:
        st.error("""
        ❌ **CREDENCIAIS NÃO CONFIGURADAS!**

        Para usar o RoboWordpress, você precisa configurar as credenciais no Streamlit Cloud.
        """)

        with st.expander("🔧 **COMO CONFIGURAR - CLIQUE AQUI**", expanded=True):
            st.markdown("""
            ### 📋 **PASSOS PARA CONFIGURAR:**

            1. **Acesse:** https://share.streamlit.io
            2. **Encontre seu app** RoboWordpress
            3. **Clique no menu "⋮"** (três pontos)
            4. **Selecione "Settings"**
            5. **Clique na aba "Secrets"**
            6. **Cole este texto** (substitua pelos seus valores):

            ```toml
            WP_URL = "https://seu-site-wordpress.com"
            WP_USER = "seu_usuario"
            WP_PASSWORD = "sua_senha"
            OPENAI_API_KEY = "sk-proj-sua-chave..."
            ```

            7. **Clique "Save"**
            8. **Reinicie o app** (botão "Reboot")
            """)

            st.info("📋 **Credenciais faltando:** " + ", ".join(missing_secrets))

        st.warning("⚠️ Configure as credenciais acima para continuar usando o app.")
        st.stop()
    else:
        st.success("✅ **Credenciais configuradas com sucesso!**")

else:
    st.info("💻 **Rodando localmente** - Configure o arquivo `.env`")

st.markdown("---")

# Sidebar com informações
st.sidebar.markdown("## 📊 Status do Sistema")

# Verificar configurações
def verificar_configuracoes():
    """Verifica se todas as configurações estão corretas"""
    try:
        # Pegar credenciais WordPress da sessão autenticada
        WP_URL = st.session_state.get('wp_url', '')
        WP_USER = st.session_state.get('wp_user', '')
        WP_PASSWORD = st.session_state.get('wp_password', '')
        
        # Pegar OpenAI das configurações
        if is_streamlit_cloud:
            OPENAI_API_KEY = st.secrets.get('OPENAI_API_KEY', '')
        else:
            # Importar config local
            sys.path.append(os.getcwd())
            try:
                from config import OPENAI_API_KEY
            except ImportError:
                OPENAI_API_KEY = ''

        # Verificações essenciais
        wp_ok = bool(WP_URL and WP_USER and WP_PASSWORD)
        openai_ok = OPENAI_API_KEY and len(OPENAI_API_KEY) > 20 and OPENAI_API_KEY.startswith('sk-')

        status = {
            'wordpress': wp_ok,
            'openai': openai_ok
        }

        return status, {
            'wp_url': WP_URL,
            'wp_user': WP_USER,
            'openai_key': f"{OPENAI_API_KEY[:15]}..." if OPENAI_API_KEY and len(OPENAI_API_KEY) > 15 else "Não configurada"
        }
    except Exception as e:
        return None, f"Erro ao carregar configurações: {str(e)}"

# Sidebar com informações
st.sidebar.markdown("## 📊 Status do Sistema")

# Verificar status baseado na sessão autenticada
status, config_info = verificar_configuracoes()

if status:
    # Exibir status na sidebar
    st.sidebar.markdown("### 🔧 Configurações")
    
    for key, value in status.items():
        icon = "✅" if value else "❌"
        labels = {
            'wordpress': 'WordPress',
            'openai': 'OpenAI'
        }
        st.sidebar.markdown(f"{icon} {labels[key]}")
    
    if isinstance(config_info, dict):
        st.sidebar.markdown("### 📋 Detalhes")
        st.sidebar.markdown(f"**Site:** {config_info['wp_url']}")
        st.sidebar.markdown(f"**Usuário:** {config_info['wp_user']}")
        st.sidebar.markdown("**Tópicos:** Configurados na interface")
        
        # Mostrar dados carregados do WordPress
        if 'wp_autores' in st.session_state:
            st.sidebar.markdown(f"**Autores:** {len(st.session_state.wp_autores)} encontrados")
        if 'wp_categorias' in st.session_state:
            st.sidebar.markdown(f"**Categorias:** {len(st.session_state.wp_categorias)} encontradas")
else:
    st.sidebar.error(f"⚠️ {config_info}")

# Função para executar comandos
def executar_comando(comando, nome_processo):
    """Executa um comando e retorna o resultado"""
    try:
        # Ativar ambiente virtual e executar comando
        cmd_completo = f"source venv/bin/activate && {comando}"
        result = subprocess.run(cmd_completo, shell=True, capture_output=True, text=True, timeout=300)
        
        return {
            'sucesso': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'codigo': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'sucesso': False,
            'stdout': '',
            'stderr': 'Processo excedeu tempo limite (5 minutos)',
            'codigo': -1
        }
    except Exception as e:
        return {
            'sucesso': False,
            'stdout': '',
            'stderr': f'Erro ao executar: {str(e)}',
            'codigo': -1
        }

# Função para executar comando com logs em tempo real
def executar_comando_com_logs(comando, nome_processo, log_container):
    """Executa um comando mostrando logs em tempo real"""
    import subprocess
    import time
    from datetime import datetime
    
    # Mostrar início da execução
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_container.info(f"🚀 [{timestamp}] Iniciando execução do {nome_processo}...")
    
    # Contador de tempo de execução
    inicio_execucao = datetime.now()
    contador_tempo = log_container.empty()
    
    # Contador de posts criados (exibir desde o início)
    contador_posts = log_container.empty()
    posts_criados = 0
    contador_posts.metric("📝 Posts criados", f"{posts_criados} posts")
    
    # Barra de progresso
    progress_bar = log_container.progress(0)
    progress_text = log_container.empty()
    
    try:
        # Comando completo: usar o mesmo interpretador Python do Streamlit
        cmd_completo = f"{sys.executable} {comando}"
        # Forçar working directory correto no Streamlit Cloud
        process = subprocess.Popen(
            cmd_completo,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd="/mount/src/robowordpress" if is_streamlit_cloud else None
        )
        
        # Placeholder para logs em tempo real
        log_placeholder = log_container.empty()
        logs_completos = []
        linha_count = 0
        
        # Ler saída linha por linha
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                timestamp = datetime.now().strftime("%H:%M:%S")
                linha_log = f"[{timestamp}] {output.strip()}"
                logs_completos.append(linha_log)
                linha_count += 1
                
                # Atualizar progresso baseado no conteúdo dos logs
                if "[LOG]" in output or "PROCESSANDO TÓPICO" in output:
                    progress = min(linha_count * 3, 85)  # Incremento maior para logs importantes
                else:
                    progress = min(linha_count * 1, 85)
                progress_bar.progress(progress)
                
                # Atualizar contador de tempo
                tempo_decorrido = datetime.now() - inicio_execucao
                minutos, segundos = divmod(tempo_decorrido.total_seconds(), 60)
                contador_tempo.metric("⏱️ Tempo de execução", f"{int(minutos):02d}:{int(segundos):02d}")
                
                # Atualizar contador de posts quando detectar publicação
                if any(indicador in output for indicador in [
                    "Post publicado com sucesso",
                    "publicado com ID", 
                    "[RESULTADO] Post publicado",
                    "✔] Post publicado",
                    "✔] Post criado",
                    "✅ Post publicado",
                    "RESULTADO] ✅ Post publicado"
                ]):
                    posts_criados += 1
                    contador_posts.metric("📝 Posts criados", f"{posts_criados} posts")
                    # Log adicional para debug
                    timestamp_debug = datetime.now().strftime("%H:%M:%S")
                    print(f"[DEBUG {timestamp_debug}] Contador incrementado para {posts_criados} - Detectado: {output.strip()[:100]}")
                
                # Mensagens de status específicas baseadas no conteúdo
                if "Iniciando geração de título" in output:
                    progress_text.text("🎯 Gerando título...")
                elif "Título gerado" in output or "✅ Título gerado" in output:
                    progress_text.text("✅ Título criado! Gerando artigo...")
                elif "Iniciando geração do artigo" in output:
                    progress_text.text("📝 Criando artigo... (pode levar até 90s)")
                elif "Tentativa" in output and "Gerando artigo" in output:
                    progress_text.text("🔄 Tentando gerar artigo novamente...")
                elif "Artigo gerado" in output or "✅ Artigo gerado" in output:
                    progress_text.text("✅ Artigo criado! Publicando...")
                elif "Iniciando publicação" in output or "Publicando post" in output:
                    progress_text.text("🚀 Publicando no WordPress...")
                elif "timeout" in output.lower():
                    progress_text.text("⏰ Timeout detectado - tentando novamente...")
                elif "rate limit" in output.lower():
                    progress_text.text("⏳ Rate limit - aguardando...")
                elif any(indicador in output for indicador in ["Post publicado", "✅ Post publicado", "RESULTADO] ✅"]):
                    progress_text.text(f"🎉 Post criado com sucesso! Total: {posts_criados}")
                elif "ERRO" in output and "Falha ao processar" in output:
                    progress_text.text("❌ Erro processando tópico - continuando...")
                elif "sucesso" in output.lower():
                    progress_text.text("✅ Operação realizada com sucesso!")
                else:
                    progress_text.text(f"📊 Processando... ({linha_count} linhas)")
                
                # Mostrar últimas 10 linhas
                ultimas_linhas = logs_completos[-10:]
                log_text = "\n".join(ultimas_linhas)
                log_placeholder.code(log_text, language="text")
        
        # Esperar processo terminar
        return_code = process.wait()
        
        # Finalizar progresso
        progress_bar.progress(100)
        
        # Resultado final
        timestamp = datetime.now().strftime("%H:%M:%S")
        tempo_total = datetime.now() - inicio_execucao
        minutos, segundos = divmod(tempo_total.total_seconds(), 60)
        
        if return_code == 0:
            progress_text.text("✅ Execução concluída com sucesso!")
            contador_tempo.metric("⏱️ Tempo total", f"{int(minutos):02d}:{int(segundos):02d}")
            contador_posts.metric("📝 Posts criados", f"{posts_criados} posts")
            
            # Resumo final detalhado
            if posts_criados > 0:
                log_container.success(f"✅ [{timestamp}] {nome_processo} executado com sucesso!")
                col1, col2, col3 = log_container.columns(3)
                with col1:
                    st.metric("⏱️ Tempo total", f"{int(minutos):02d}:{int(segundos):02d}")
                with col2:
                    st.metric("📝 Posts criados", f"{posts_criados}")
                with col3:
                    if posts_criados > 0:
                        tempo_por_post = tempo_total.total_seconds() / posts_criados
                        st.metric("⚡ Tempo/post", f"{tempo_por_post:.1f}s")
            else:
                log_container.warning(f"⚠️ [{timestamp}] {nome_processo} executado, mas nenhum post foi criado")
            
            return {
                'sucesso': True,
                'stdout': '\n'.join(logs_completos),
                'stderr': '',
                'codigo': return_code,
                'posts_criados': posts_criados
            }
        else:
            progress_text.text("❌ Execução falhou!")
            contador_tempo.metric("⏱️ Tempo até falha", f"{int(minutos):02d}:{int(segundos):02d}")
            contador_posts.metric("📝 Posts criados", f"{posts_criados} posts")
            log_container.error(f"❌ [{timestamp}] {nome_processo} falhou com código {return_code} após {int(minutos):02d}:{int(segundos):02d}. Posts criados: {posts_criados}")
            return {
                'sucesso': False,
                'stdout': '\n'.join(logs_completos),
                'stderr': f'Processo falhou com código {return_code}',
                'codigo': return_code
            }
            
    except subprocess.TimeoutExpired:
        timestamp = datetime.now().strftime("%H:%M:%S")
        tempo_total = datetime.now() - inicio_execucao
        minutos, segundos = divmod(tempo_total.total_seconds(), 60)
        progress_bar.progress(0)
        progress_text.text("⏰ Tempo limite excedido!")
        contador_tempo.metric("⏱️ Tempo até timeout", f"{int(minutos):02d}:{int(segundos):02d}")
        log_container.error(f"⏰ [{timestamp}] {nome_processo} excedeu tempo limite após {int(minutos):02d}:{int(segundos):02d}!")
        return {
            'sucesso': False,
            'stdout': '',
            'stderr': 'Processo excedeu tempo limite (5 minutos)',
            'codigo': -1
        }
    except Exception as e:
        timestamp = datetime.now().strftime("%H:%M:%S")
        tempo_total = datetime.now() - inicio_execucao
        minutos, segundos = divmod(tempo_total.total_seconds(), 60)
        progress_bar.progress(0)
        progress_text.text(f"💥 Erro na execução!")
        contador_tempo.metric("⏱️ Tempo até erro", f"{int(minutos):02d}:{int(segundos):02d}")
        log_container.error(f"💥 [{timestamp}] Erro ao executar {nome_processo} após {int(minutos):02d}:{int(segundos):02d}: {str(e)}")
        return {
            'sucesso': False,
            'stdout': '',
            'stderr': f'Erro ao executar: {str(e)}',
            'codigo': -1
        }

# Importar módulo de prompts
try:
    from prompt_manager import carregar_prompts, salvar_prompts, validar_prompts
except ImportError:
    st.error("Erro ao importar módulo de prompts. Verifique se prompt_manager.py existe.")
    st.stop()

# Layout principal
st.markdown("## 📝 Editor de Prompts Personalizáveis")

# Editor de prompts em destaque
with st.expander("🎯 CONFIGURE OS PROMPTS DA IA - Clique para abrir", expanded=True):
    st.markdown("""
    ### 🔧 Personalize como a IA gera conteúdo
    
    **🎯 IMPORTANTE:** Use o **Robô Personalizável (v3)** para aplicar os prompts editados aqui.
    
    Controle como a IA:
    - **🎭 Gera títulos** baseados nos tópicos da planilha
    - **📝 Cria artigos** completos e otimizados para SEO
    """)
    
    # Carregar prompts atuais
    prompts_atuais = carregar_prompts()
    
    # Tabs para organizar os prompts
    tab_titulo, tab_artigo = st.tabs(["📰 Prompt para Títulos", "📄 Prompt para Artigos"])
    
    with tab_titulo:
        st.markdown("### 📰 Como a IA deve gerar títulos")
        st.markdown("**Variável disponível:** `{topico_geral}` (será substituído pelo tópico da planilha)")
        
        prompt_titulo_novo = st.text_area(
            "Edite o prompt do título:",
            value=prompts_atuais.get('prompt_titulo', ''),
            height=250,
            help="Este prompt controla como a IA gera títulos baseados no tópico da planilha Google Sheets",
            key="prompt_titulo_main"
        )
        
        # System prompt para título
        system_titulo_novo = st.text_area(
            "Personalidade da IA para títulos:",
            value=prompts_atuais.get('system_prompt_titulo', ''),
            height=80,
            help="Define como a IA deve se comportar ao gerar títulos",
            key="system_titulo_main"
        )
    
    with tab_artigo:
        st.markdown("### 📄 Como a IA deve gerar artigos completos")
        st.markdown("**Variáveis disponíveis:** `{titulo_especifico}` (título gerado) e `{topico_geral}` (tópico da planilha)")
        
        prompt_artigo_novo = st.text_area(
            "Edite o prompt do artigo:",
            value=prompts_atuais.get('prompt_artigo', ''),
            height=300,
            help="Este prompt controla como a IA escreve artigos completos baseados no título gerado",
            key="prompt_artigo_editor"
        )
        
        # System prompt para artigo
        system_artigo_novo = st.text_area(
            "Personalidade da IA para artigos:",
            value=prompts_atuais.get('system_prompt_artigo', ''),
            height=80,
            help="Define como a IA deve se comportar ao gerar artigos",
            key="system_artigo_editor"
        )
    
    # Botões de ação em destaque
    col_save, col_preview, col_reset = st.columns(3)
    
    with col_save:
        if st.button("💾 SALVAR PROMPTS", type="primary", use_container_width=True):
            novos_prompts = {
                'prompt_titulo': prompt_titulo_novo,
                'prompt_artigo': prompt_artigo_novo,
                'system_prompt_titulo': system_titulo_novo,
                'system_prompt_artigo': system_artigo_novo
            }
            
            # Validar prompts
            erros = validar_prompts(novos_prompts)
            
            if erros:
                st.error("❌ Erros encontrados nos prompts:")
                for campo, erro in erros.items():
                    st.error(f"**{campo}:** {erro}")
            else:
                if salvar_prompts(novos_prompts):
                    st.success("✅ Prompts salvos com sucesso!")
                    st.success("🎯 Use o 'Robô Personalizável (v3)' para aplicar os novos prompts!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar prompts.")
    
    with col_preview:
        if st.button("👀 PREVIEW", use_container_width=True):
            st.markdown("### 🔍 Preview dos Prompts")
            
            exemplo_topico = "Filmes e Cinema"
            exemplo_titulo = "Os 10 Filmes Mais Aguardados de 2025"
            
            st.markdown("**📰 Preview Prompt Título:**")
            try:
                preview_titulo = prompt_titulo_novo.format(topico_geral=exemplo_topico)
                st.code(preview_titulo[:300] + "..." if len(preview_titulo) > 300 else preview_titulo)
            except Exception as e:
                st.error(f"Erro no prompt título: {e}")
            
            st.markdown("**📄 Preview Prompt Artigo:**")
            try:
                preview_artigo = prompt_artigo_novo.format(
                    titulo_especifico=exemplo_titulo,
                    topico_geral=exemplo_topico
                )
                st.code(preview_artigo[:400] + "..." if len(preview_artigo) > 400 else preview_artigo)
            except Exception as e:
                st.error(f"Erro no prompt artigo: {e}")
    
    with col_reset:
        if st.button("🔄 Restaurar Padrão", use_container_width=True):
            if st.session_state.get('confirm_reset'):
                # Carregar prompts padrão
                from prompt_manager import get_prompts_padrao
                prompts_padrao = get_prompts_padrao()
                
                if salvar_prompts(prompts_padrao):
                    st.success("✅ Prompts restaurados para o padrão!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Erro ao restaurar prompts.")
                
                st.session_state['confirm_reset'] = False
            else:
                st.session_state['confirm_reset'] = True
                st.warning("⚠️ Clique novamente para confirmar a restauração.")

# Separador
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 🚀 Executar Robôs")
    
    # Usar credenciais da sessão autenticada
    wp_url = st.session_state.wp_url
    wp_user = st.session_state.wp_user 
    wp_password = st.session_state.wp_password
    credenciais_ok = True  # Já validado no login
    
    st.markdown("---")
    
    # Configurações para execução
    st.markdown("### ⚙️ Configurações de Execução")
    
    # Campo para inserir tópicos diretamente
    st.markdown("#### 📝 Tópicos para Gerar Conteúdo")
    topicos_input = st.text_area(
        "Digite os tópicos (um por linha):",
        value="Filmes e Cinema\nSéries de TV\nHistória e Curiosidades\nViagem e Turismo\nLivros e Literatura",
        height=120,
        help="Digite cada tópico em uma linha separada. Estes tópicos serão usados para gerar os títulos e artigos."
    )
    
    # Processar tópicos inseridos
    topicos_lista = [t.strip() for t in topicos_input.split('\n') if t.strip()]
    
    if topicos_lista:
        st.success(f"✅ {len(topicos_lista)} tópicos configurados: {', '.join(topicos_lista[:3])}{'...' if len(topicos_lista) > 3 else ''}")
    else:
        st.warning("⚠️ Adicione pelo menos um tópico para continuar")
    
    st.markdown("---")
    
    # Importar função utilitária com tratamento de erro
    try:
        from app_utils import buscar_autores_wordpress, buscar_categorias_wordpress, buscar_usuario_atual
    except ImportError as e:
        st.error(f"Erro ao importar app_utils: {e}")
        # Função alternativa simples em caso de erro
        def buscar_autores_wordpress(wp_url, wp_user, wp_password):
            return []
        def buscar_categorias_wordpress(wp_url, wp_user, wp_password):
            return [(32174, "mundo (ID: 32174)"), (1, "Uncategorized"), (0, "Others")]
        def buscar_usuario_atual(wp_url, wp_user, wp_password):
            return None
    
    # Carregar dados do WordPress automaticamente (usando credenciais da sessão)
    if 'wp_autores' not in st.session_state or 'wp_categorias' not in st.session_state:
        with st.spinner("🔄 Carregando dados do WordPress..."):
            try:
                # Debug: mostrar credenciais sendo usadas (sem a senha)
                st.info(f"🔍 Conectando em: {wp_url} como {wp_user}")
                
                # Buscar autores (tentar múltiplas abordagens)
                st.session_state.wp_autores = buscar_autores_wordpress(wp_url, wp_user, wp_password)
                
                # Se não conseguiu buscar lista de autores, tentar buscar apenas o usuário atual como último recurso
                if not st.session_state.wp_autores:
                    st.warning("⚠️ Não foi possível carregar lista completa de autores")
                    st.info("🔄 Tentando buscar pelo menos o usuário atual...")
                    usuario_atual = buscar_usuario_atual(wp_url, wp_user, wp_password)
                    if usuario_atual:
                        st.session_state.wp_autores = [usuario_atual]
                        st.info(f"✅ Carregado usuário atual: {usuario_atual[1]} (ID: {usuario_atual[0]})")
                        st.info("💡 **Nota:** Para ver todos os autores, o usuário precisa ter permissões de administrador")
                
                # Buscar categorias
                st.session_state.wp_categorias = buscar_categorias_wordpress(wp_url, wp_user, wp_password)
                
                # Mostrar resultados detalhados
                if st.session_state.wp_autores:
                    if len(st.session_state.wp_autores) == 1:
                        # Apenas um autor (usuário atual)
                        autor_id, autor_nome = st.session_state.wp_autores[0]
                        st.success(f"✅ Autor identificado: {autor_nome} (ID: {autor_id})")
                        st.warning("⚠️ **Permissões limitadas:** Seu usuário só pode ver a si mesmo")
                        st.info("💡 **Solução:** O ID 210 será adicionado automaticamente como opção padrão")
                    else:
                        # Múltiplos autores carregados
                        st.success(f"✅ Carregados {len(st.session_state.wp_autores)} autores do WordPress")
                        autores_nomes = [nome for id, nome in st.session_state.wp_autores]
                        st.info(f"👥 Autores encontrados: {', '.join(autores_nomes)}")
                        
                        # Verificar se ID 210 está na lista
                        if 210 in [id for id, nome in st.session_state.wp_autores]:
                            st.success("🎯 **Autor padrão (ID 210) encontrado na lista!**")
                        else:
                            st.info("🎯 **Autor padrão (ID 210) será adicionado à lista**")
                else:
                    st.warning("⚠️ Não foi possível carregar autores do WordPress")
                    st.info("🎯 **Não se preocupe:** O ID 210 será usado como padrão automaticamente")
                    st.info("💡 **Causa:** Usuário com permissões limitadas (normal para segurança)")
                
                if st.session_state.wp_categorias:
                    st.success(f"✅ Carregadas {len(st.session_state.wp_categorias)} categorias do WordPress")
                    # Debug: mostrar algumas categorias com IDs
                    categorias_debug = [f"{nome} (ID: {id})" for id, nome in st.session_state.wp_categorias[:5]]
                    st.info(f"📁 Primeiras categorias: {', '.join(categorias_debug)}")
                    
                    # Verificar se categoria 32174 está na lista
                    if 32174 in [id for id, nome in st.session_state.wp_categorias]:
                        st.success("🎯 **Categoria padrão (32174 - mundo) encontrada na lista!**")
                    else:
                        st.info("🎯 **Categoria padrão (32174 - mundo) será adicionada à lista**")
                else:
                    st.warning("⚠️ Nenhuma categoria encontrada - usando padrões")
                    # Definir categorias padrão
                    st.session_state.wp_categorias = [(32174, "mundo (ID: 32174)"), (1, "Uncategorized"), (0, "Others")]
                    
            except Exception as e:
                st.error(f"❌ Erro ao carregar dados do WordPress: {e}")
                st.session_state.wp_autores = []
                st.session_state.wp_categorias = [(32174, "mundo (ID: 32174)"), (1, "Uncategorized"), (0, "Others")]
                
    # Botão para recarregar dados se necessário
    if st.button("🔄 Recarregar Dados do WordPress", help="Clique se os autores/categorias não apareceram"):
        # Limpar cache e recarregar
        if 'wp_autores' in st.session_state:
            del st.session_state.wp_autores
        if 'wp_categorias' in st.session_state:
            del st.session_state.wp_categorias
        st.rerun()
    
    # Configurações para execução (agora usando dados carregados automaticamente)
    st.markdown("### ⚙️ Configurações de Execução")
    
    col_config1, col_config2, col_config3, col_config4 = st.columns(4)

    with col_config1:
        if st.session_state.wp_categorias:
            # Se conseguimos carregar categorias, mostrar lista com IDs
            categoria_options = {f"{nome} (ID: {id})": id for id, nome in st.session_state.wp_categorias}
            
            # Adicionar manualmente a categoria 32174 se não estiver na lista
            if 32174 not in [id for id, nome in st.session_state.wp_categorias]:
                categoria_options["mundo (ID: 32174) - PADRÃO"] = 32174
                st.info("✅ Categoria padrão (32174 - mundo) adicionada à lista")
            
            # Procurar se o ID 32174 existe na lista para definir como padrão
            default_index = 0
            categoria_32174_key = None
            for key, cat_id in categoria_options.items():
                if cat_id == 32174:
                    categoria_32174_key = key
                    break
            
            # Se encontrou o ID 32174, definir como padrão
            if categoria_32174_key:
                options_list = list(categoria_options.keys())
                default_index = options_list.index(categoria_32174_key)
            
            categoria_selecionada = st.selectbox(
                "📁 Categoria WordPress:",
                options=list(categoria_options.keys()),
                index=default_index,
                help="Categoria onde os posts serão publicados. Padrão: 32174 (mundo)"
            )
            categoria_wp_id = categoria_options[categoria_selecionada]
            
            # Mostrar informação sobre a categoria selecionada
            if categoria_wp_id == 32174:
                st.success("🎯 **Categoria padrão (32174 - mundo) selecionada**")
            else:
                st.info(f"📁 Categoria selecionada: ID {categoria_wp_id}")
        else:
            # Se não conseguimos carregar categorias, usar ID 32174 como padrão
            st.markdown("📁 **Categoria WordPress:**")
            categoria_wp_id = st.number_input(
                "ID da Categoria:",
                min_value=1,
                value=32174,  # ID 32174 como padrão
                help="Digite o ID da categoria no WordPress. Padrão: 32174 (mundo)"
            )
            
            if categoria_wp_id == 32174:
                st.success("🎯 **Usando categoria padrão (32174 - mundo)**")
            else:
                st.info(f"📁 Categoria personalizada: ID {categoria_wp_id}")

    with col_config2:
        status_publicacao = st.selectbox(
            "📮 Status de Publicação:",
            ["draft", "publish"],
            index=0,
            help="Escolha se os posts serão salvos como rascunho ou publicados diretamente"
        )

    with col_config3:
        quantidade_maxima = min(len(topicos_lista), 10) if topicos_lista else 3
        quantidade_textos = st.number_input(
            "📝 Quantidade de Textos:",
            min_value=1,
            max_value=quantidade_maxima,
            value=min(3, quantidade_maxima),
            help=f"Número de textos que serão gerados (máximo: {quantidade_maxima} baseado nos tópicos inseridos)"
        )

    with col_config4:
        if st.session_state.wp_autores:
            # Se conseguimos carregar autores, mostrar lista
            autor_options = {f"{nome} (ID: {id})": id for id, nome in st.session_state.wp_autores}
            
            # Adicionar manualmente o ID 210 se não estiver na lista
            if 210 not in [id for id, nome in st.session_state.wp_autores]:
                autor_options["Autor Padrão (ID: 210)"] = 210
                st.info("✅ Autor padrão (ID 210) adicionado à lista")
            
            # Procurar se o ID 210 existe na lista
            default_index = 0
            autor_210_key = None
            for key, autor_id in autor_options.items():
                if autor_id == 210:
                    autor_210_key = key
                    break
            
            # Se encontrou o ID 210, definir como padrão
            if autor_210_key:
                options_list = list(autor_options.keys())
                default_index = options_list.index(autor_210_key)
            
            autor_selecionado = st.selectbox(
                "👤 Autor do Post:",
                options=list(autor_options.keys()),
                index=default_index,
                help="Autor que será atribuído ao post no WordPress. Padrão: ID 210"
            )
            author_id = autor_options[autor_selecionado]
            
            # Mostrar informação sobre o autor selecionado
            if author_id == 210:
                st.success("🎯 **Autor padrão (ID 210) selecionado**")
            else:
                st.info(f"👤 Autor selecionado: ID {author_id}")
        else:
            # Se não conseguimos carregar autores, usar ID 210 como padrão
            st.markdown("👤 **Autor do Post:**")
            author_id = st.number_input(
                "ID do Autor:",
                min_value=1,
                value=210,  # ID 210 como padrão
                help="Digite o ID do autor no WordPress. Padrão: 210"
            )
            
            if author_id == 210:
                st.success("🎯 **Usando autor padrão (ID 210)**")
            else:
                st.info(f"👤 Autor personalizado: ID {author_id}")
            
            with st.expander("ℹ️ Sobre permissões de usuário"):
                st.markdown("""
                **Por que não conseguimos listar todos os autores?**
                
                🔐 **Seu usuário atual tem permissões limitadas:**
                - Pode acessar apenas as próprias informações
                - Não pode listar outros usuários do WordPress
                - Isso é uma configuração de segurança normal
                
                **✅ Soluções:**
                1. **Use o ID 210 (padrão)** - já configurado automaticamente
                2. **Para ver todos os autores:** solicite ao administrador para:
                   - Promover seu usuário a Editor ou Admin
                   - Ou criar um Application Password de usuário com mais permissões
                
                **🎯 O ID 210 funcionará normalmente** para publicar posts!
                """)

    # Salvar configurações na sessão
    st.session_state['categoria_wp'] = categoria_wp_id
    st.session_state['status_publicacao'] = status_publicacao
    st.session_state['quantidade_textos'] = quantidade_textos
    st.session_state['topicos_lista'] = topicos_lista[:quantidade_textos]  # Limitar aos selecionados
    st.session_state['author_id'] = author_id
    
    st.markdown("---")
    
    # Cards dos robôs (somente os que vamos manter)
    robots = [
        {
            'nome': 'Robô com Imagens IA (v4) ✨ NOVO!',
            'arquivo': 'robo_pilloto_v4.py',
            'descricao': 'Gera conteúdo + imagens automáticas com DALL·E 3 e define como imagem em destaque',
            'icon': '🎨'
        },
        {
            'nome': 'Robô Personalizável (v3)',
            'arquivo': 'robo_pilloto_v3.py',
            'descricao': 'Versão que usa os prompts personalizáveis da interface',
            'icon': '🎯'
        },
        {
            'nome': 'Robo Piloto (Original)',
            'arquivo': 'robo_pilloto.py',
            'descricao': 'Versão alternativa com funcionalidades extras',
            'icon': '🔧'
        }
    ]
    
    for robot in robots:
        with st.container():
            st.markdown(f'<div class="robot-card">', unsafe_allow_html=True)

            col_robot1, col_robot2 = st.columns([3, 1])

            with col_robot1:
                st.markdown(f"### {robot['icon']} {robot['nome']}")
                st.markdown(f"*{robot['descricao']}*")
                st.markdown(f"**Arquivo:** `{robot['arquivo']}`")

            with col_robot2:
                if st.button(f"▶️ Executar", key=f"btn_{robot['arquivo']}", use_container_width=True):
                    if not topicos_lista:
                        st.warning("⚠️ Adicione pelo menos um tópico antes de executar!")
                    else:
                        # Verificar se OpenAI está configurada
                        try:
                            if is_streamlit_cloud:
                                openai_key = st.secrets.get('OPENAI_API_KEY', '')
                            else:
                                try:
                                    from config import OPENAI_API_KEY
                                    openai_key = OPENAI_API_KEY
                                except ImportError:
                                    openai_key = ''
                            
                            if not openai_key or len(openai_key) < 20:
                                st.error("❌ Chave da OpenAI não configurada! Configure no arquivo .env ou secrets do Streamlit.")
                                continue
                        except Exception as e:
                            st.error(f"❌ Erro ao verificar OpenAI: {e}")
                            continue
                        # Nova lógica: gerar N textos para cada tópico
                        try:
                            topicos_expandidos = []
                            for topico in topicos_lista:
                                topicos_expandidos.extend([topico] * int(quantidade_textos))
                            
                            # Criar lista formatada corretamente
                            topicos_formatados = '", "'.join(topicos_expandidos)
                            
                            config_exec_code = (
                                "# Configurações de execução vindas do app.py\n"
                                "# Este arquivo é gerado automaticamente pelo app.py\n\n"
                                f"CATEGORIA_WP = {categoria_wp_id}\n"
                                f"STATUS_PUBLICACAO = \"{status_publicacao}\"  # 'draft' ou 'publish'\n"
                                f"QUANTIDADE_TEXTOS = {quantidade_textos}\n"
                                f"TOPICOS_LISTA = [\"{topicos_formatados}\"]\n"
                                f"AUTHOR_ID = {author_id}\n\n"
                                "# Credenciais WordPress da interface\n"
                                f"WP_URL = \"{wp_url}\"\n"
                                f"WP_USER = \"{wp_user}\"\n"
                                f"WP_PASSWORD = \"{wp_password}\"\n\n"
                                "def get_configuracoes_execucao():\n"
                                "    return {\n"
                                "        'categoria_wp': CATEGORIA_WP,\n"
                                "        'status_publicacao': STATUS_PUBLICACAO,\n"
                                "        'quantidade_textos': QUANTIDADE_TEXTOS,\n"
                                "        'topicos_lista': TOPICOS_LISTA,\n"
                                "        'author_id': AUTHOR_ID,\n"
                                "        'wp_url': WP_URL,\n"
                                "        'wp_user': WP_USER,\n"
                                "        'wp_password': WP_PASSWORD\n"
                                "    }\n\n"
                                "def set_configuracoes_execucao(categoria_wp=\"Others\", status_publicacao=\"draft\", quantidade_textos=3, topicos_lista=None, author_id=1):\n"
                                "    global CATEGORIA_WP, STATUS_PUBLICACAO, QUANTIDADE_TEXTOS, TOPICOS_LISTA, AUTHOR_ID\n"
                                "    CATEGORIA_WP = categoria_wp\n"
                                "    STATUS_PUBLICACAO = status_publicacao\n"
                                "    QUANTIDADE_TEXTOS = quantidade_textos\n"
                                "    AUTHOR_ID = author_id\n"
                                "    if topicos_lista:\n"
                                "        TOPICOS_LISTA = topicos_lista\n"
                            )
                            with open('config_execucao.py', 'w') as f:
                                f.write(config_exec_code)
                        except Exception as e:
                            st.error(f"Erro ao salvar configurações: {e}")

                        # Container para logs em tempo real
                        log_container = st.container()

                        st.info(f"🎯 Executando com: Categoria={categoria_wp_id}, Status={status_publicacao}, Tópicos={len(topicos_expandidos)} (N tópicos x {quantidade_textos} textos)")
                        st.info(f"📝 Debug: Lista expandida tem {len(topicos_expandidos)} entradas: {topicos_expandidos[:3]}{'...' if len(topicos_expandidos) > 3 else ''}")

                        # Executar o robô com logs em tempo real
                        resultado = executar_comando_com_logs(robot['arquivo'], robot['nome'], log_container)

                        # Mostrar output detalhado se houver
                        if resultado['stdout']:
                            with st.expander("📋 Ver log completo da execução"):
                                st.code(resultado['stdout'], language="text")

            st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("## 🧪 Testes")
    
    # Testes disponíveis
    testes = [
        {
            'nome': 'Teste WordPress',
            'arquivo': 'teste_conexao_wordpress.py',
            'descricao': 'Verifica conexão com WordPress'
        },
        {
            'nome': 'Teste OpenAI + WordPress',
            'arquivo': 'teste_wordpress.py',
            'descricao': 'Teste completo com IA'
        }
    ]
    
    for teste in testes:
        st.markdown(f"### 🔍 {teste['nome']}")
        st.markdown(f"*{teste['descricao']}*")
        
        if st.button(f"🧪 Executar Teste", key=f"test_{teste['arquivo']}", use_container_width=True):
            # Container para logs em tempo real do teste
            log_container = st.container()
            
            # Executar teste com logs em tempo real
            resultado = executar_comando_com_logs(teste['arquivo'], teste['nome'], log_container)
            
            # Mostrar log completo se houver
            if resultado['stdout']:
                with st.expander("� Log completo do teste"):
                    st.code(resultado['stdout'], language="text")
        
        st.markdown("---")

# Seção de configuração
st.markdown("## ⚙️ Configuração")

with st.expander("🔧 Configurar Credenciais"):
    st.markdown("""
    ### Como configurar:
    
    1. **Edite o arquivo `.env`:**
    ```bash
    nano .env
    ```
    
    2. **Configure suas credenciais:**
    - `WP_URL`: URL do seu site WordPress
    - `WP_USER`: Usuário do WordPress
    - `WP_PASSWORD`: Senha ou Application Password
    - `OPENAI_API_KEY`: Sua chave da OpenAI
    
    **📝 Nota:** Os tópicos agora são configurados diretamente na interface web acima, não precisando mais do Google Sheets!
    """)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <h4>🤖 RoboWordpress <span style='color:#1f77b4;'>v{APP_VERSION}</span></h4>
    <p>Automação inteligente para WordPress com OpenAI e Google Sheets</p>
    <p><small>Desenvolvido para facilitar a criação de conteúdo SEO</small></p>
</div>
""", unsafe_allow_html=True)
