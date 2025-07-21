# Configurações de execução vindas do app.py
# Este arquivo é gerado automaticamente pelo app.py

CATEGORIA_ID = 32174
STATUS_PUBLICACAO = "draft"  # 'draft' ou 'publish'
QUANTIDADE_TEXTOS = 1
TOPICOS_LISTA = ["Tecnologia 2025"]
AUTHOR_ID = 1

# Credenciais WordPress da interface (TEMPORÁRIO PARA TESTE)
WP_URL = "https://mundodoelhmombre.com"
WP_USER = "elhmombre"
WP_PASSWORD = "hd5G t0dB wSCu f9pS IQjV bm8W"

def get_configuracoes_execucao():
    return {
        'categoria_id': CATEGORIA_ID,
        'status_publicacao': STATUS_PUBLICACAO,
        'quantidade_textos': QUANTIDADE_TEXTOS,
        'topicos_lista': TOPICOS_LISTA,
        'author_id': AUTHOR_ID,
        'wp_url': WP_URL,
        'wp_user': WP_USER,
        'wp_password': WP_PASSWORD
    }

def set_configuracoes_execucao(status_publicacao="draft", quantidade_textos=3, topicos_lista=None, author_id=1, categoria_id=1):
    global STATUS_PUBLICACAO, QUANTIDADE_TEXTOS, TOPICOS_LISTA, AUTHOR_ID, CATEGORIA_ID
    STATUS_PUBLICACAO = status_publicacao
    QUANTIDADE_TEXTOS = quantidade_textos
    AUTHOR_ID = author_id
    CATEGORIA_ID = categoria_id
    if topicos_lista:
        TOPICOS_LISTA = topicos_lista
