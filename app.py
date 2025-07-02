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
APP_VERSION = "1.0.2 - Streamlit Cloud Patch 2025-07-02"

# Título principal com versão
st.markdown(f'<h1 class="main-header">🤖 RoboWordpress - Painel de Controle <span style="font-size:1.2rem;color:#888;">v{APP_VERSION}</span></h1>', unsafe_allow_html=True)

# ⚠️ SEÇÃO DE CONFIGURAÇÃO DESTACADA
st.markdown("---")


# Verificar se está rodando no Streamlit Cloud (método robusto)
def detect_streamlit_cloud():
    # 1. Variável de ambiente padrão do Streamlit Cloud
    if os.getenv('STREAMLIT_CLOUD', '').lower() == 'true':
        return True
    # 2. st.secrets._secrets_file é None apenas no cloud
    if hasattr(st, 'secrets') and hasattr(st.secrets, '_secrets_file'):
        if st.secrets._secrets_file is None:
            return True
    return False

is_streamlit_cloud = detect_streamlit_cloud()

if is_streamlit_cloud:
    st.markdown("## 🌐 **RODANDO NO STREAMLIT CLOUD**")
    
    # Verificar se secrets estão configuradas
    missing_secrets = []
    try:
        required_secrets = ['WP_URL', 'WP_USER', 'WP_PASSWORD', 'OPENAI_API_KEY', 'GOOGLE_SHEET_ID', 'GOOGLE_SHEET_NAME']
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
            GOOGLE_SHEET_ID = "1ABC123DEF456..."
            GOOGLE_SHEET_NAME = "Nome da Planilha"
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
        if is_streamlit_cloud:
            # Pega variáveis dos secrets do Streamlit Cloud
            WP_URL = st.secrets.get('WP_URL', '')
            WP_USER = st.secrets.get('WP_USER', '')
            WP_PASSWORD = st.secrets.get('WP_PASSWORD', '')
            OPENAI_API_KEY = st.secrets.get('OPENAI_API_KEY', '')
            GOOGLE_SHEET_NAME = st.secrets.get('GOOGLE_SHEET_NAME', st.secrets.get('GOOGLE_SHEET', ''))
            GOOGLE_SHEET_ID = st.secrets.get('GOOGLE_SHEET_ID', '')

            # Para credenciais Google: considerar válido se ambos presentes
            credentials_ok = bool(GOOGLE_SHEET_ID and GOOGLE_SHEET_NAME)
        else:
            # Importar config local
            sys.path.append(os.getcwd())
            from config import WP_URL, WP_USER, WP_PASSWORD, OPENAI_API_KEY, GOOGLE_SHEET_NAME, GOOGLE_SHEET_ID

            # Para credenciais Google: verificar se arquivo existe OU se tem credenciais nos secrets
            credentials_ok = os.path.exists('credenciais_google.json')
            try:
                if hasattr(st, 'secrets') and ('GOOGLE_CREDENTIALS' in st.secrets or 'GOOGLE_CREDENTIALS_JSON' in st.secrets):
                    credentials_ok = True
            except Exception:
                pass

        # Verificações mais flexíveis
        wp_ok = WP_URL not in ['https://exemplo.com', 'https://seu-site.com', '', None] and WP_PASSWORD not in ['senha', 'sua_senha', '', None]
        openai_ok = OPENAI_API_KEY and len(OPENAI_API_KEY) > 20 and OPENAI_API_KEY.startswith('sk-')
        sheets_ok = (GOOGLE_SHEET_NAME not in ['nome_da_sua_planilha', 'TopicosBlog', '', None]) and bool(GOOGLE_SHEET_ID)

        status = {
            'wordpress': wp_ok,
            'openai': openai_ok,
            'google_sheets': sheets_ok,
            'credentials_file': credentials_ok
        }

        return status, {
            'wp_url': WP_URL,
            'wp_user': WP_USER,
            'google_sheet': GOOGLE_SHEET_NAME,
            'openai_key': f"{OPENAI_API_KEY[:15]}..." if OPENAI_API_KEY and len(OPENAI_API_KEY) > 15 else "Não configurada"
        }
    except Exception as e:
        return None, f"Erro ao carregar configurações: {str(e)}"

# Verificar status
status, config_info = verificar_configuracoes()

if status:
    # Exibir status na sidebar
    st.sidebar.markdown("### 🔧 Configurações")
    
    for key, value in status.items():
        icon = "✅" if value else "❌"
        labels = {
            'wordpress': 'WordPress',
            'openai': 'OpenAI',
            'google_sheets': 'Google Sheets',
            'credentials_file': 'Credenciais Google'
        }
        st.sidebar.markdown(f"{icon} {labels[key]}")
    
    if isinstance(config_info, dict):
        st.sidebar.markdown("### 📋 Detalhes")
        st.sidebar.markdown(f"**Site:** {config_info['wp_url']}")
        st.sidebar.markdown(f"**Usuário:** {config_info['wp_user']}")
        st.sidebar.markdown(f"**Planilha:** {config_info['google_sheet']}")
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
    
    # Barra de progresso
    progress_bar = log_container.progress(0)
    progress_text = log_container.empty()
    
    try:
        # Comando completo
        cmd_completo = f"python {comando}"
        
        # Executar processo
        process = subprocess.Popen(
            cmd_completo,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
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
                
                # Atualizar progresso (estimativa baseada no número de linhas)
                progress = min(linha_count * 2, 90)  # Max 90% durante execução
                progress_bar.progress(progress)
                progress_text.text(f"📊 Processando... ({linha_count} linhas processadas)")
                
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
        if return_code == 0:
            progress_text.text("✅ Execução concluída com sucesso!")
            log_container.success(f"✅ [{timestamp}] {nome_processo} executado com sucesso!")
            return {
                'sucesso': True,
                'stdout': '\n'.join(logs_completos),
                'stderr': '',
                'codigo': return_code
            }
        else:
            progress_text.text("❌ Execução falhou!")
            log_container.error(f"❌ [{timestamp}] {nome_processo} falhou com código {return_code}")
            return {
                'sucesso': False,
                'stdout': '\n'.join(logs_completos),
                'stderr': f'Processo falhou com código {return_code}',
                'codigo': return_code
            }
            
    except subprocess.TimeoutExpired:
        timestamp = datetime.now().strftime("%H:%M:%S")
        progress_bar.progress(0)
        progress_text.text("⏰ Tempo limite excedido!")
        log_container.error(f"⏰ [{timestamp}] {nome_processo} excedeu tempo limite!")
        return {
            'sucesso': False,
            'stdout': '',
            'stderr': 'Processo excedeu tempo limite (5 minutos)',
            'codigo': -1
        }
    except Exception as e:
        timestamp = datetime.now().strftime("%H:%M:%S")
        progress_bar.progress(0)
        progress_text.text(f"💥 Erro na execução!")
        log_container.error(f"💥 [{timestamp}] Erro ao executar {nome_processo}: {str(e)}")
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
    
    # Cards dos robôs
    robots = [
        {
            'nome': 'Robô Principal (v2)',
            'arquivo': 'robo_pillot_v2.py',
            'descricao': 'Versão principal com todas as funcionalidades',
            'icon': '🤖'
        },
        {
            'nome': 'Robô Personalizável (v3)',
            'arquivo': 'robo_pilloto_v3.py',
            'descricao': 'Versão que usa os prompts personalizáveis da interface',
            'icon': '🎯'
        },
        {
            'nome': 'Robô Simples',
            'arquivo': 'robo_simples.py', 
            'descricao': 'Versão simplificada para testes rápidos',
            'icon': '⚡'
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
                    if status and all(status.values()):
                        # Container para logs em tempo real
                        log_container = st.container()
                        
                        # Executar o robô com logs em tempo real
                        resultado = executar_comando_com_logs(robot['arquivo'], robot['nome'], log_container)
                        
                        # Mostrar output detalhado se houver
                        if resultado['stdout']:
                            with st.expander("📋 Ver log completo da execução"):
                                st.code(resultado['stdout'], language="text")
                    else:
                        st.warning("⚠️ Configure todas as credenciais antes de executar!")
            
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
            'nome': 'Teste Google Sheets',
            'arquivo': 'teste_sheets.py',
            'descricao': 'Verifica conexão com planilha'
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
    - `GOOGLE_SHEET_NAME`: Nome da planilha Google
    
    3. **Adicione credenciais do Google:**
    - Baixe o arquivo JSON das credenciais
    - Renomeie para `credenciais_google.json`
    - Coloque na pasta do projeto
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
