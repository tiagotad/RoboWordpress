# Configurações de execução vindas do app.py
# Este arquivo é gerado automaticamente pelo app.py

# Configurações padrão
CATEGORIA_WP = "Others"
STATUS_PUBLICACAO = "draft"  # "draft" ou "publish"
QUANTIDADE_TEXTOS = 3

def get_configuracoes_execucao():
    """Retorna as configurações de execução"""
    return {
        'categoria_wp': CATEGORIA_WP,
        'status_publicacao': STATUS_PUBLICACAO,
        'quantidade_textos': QUANTIDADE_TEXTOS
    }

def set_configuracoes_execucao(categoria_wp="Others", status_publicacao="draft", quantidade_textos=3):
    """Define as configurações de execução"""
    global CATEGORIA_WP, STATUS_PUBLICACAO, QUANTIDADE_TEXTOS
    CATEGORIA_WP = categoria_wp
    STATUS_PUBLICACAO = status_publicacao
    QUANTIDADE_TEXTOS = quantidade_textos
