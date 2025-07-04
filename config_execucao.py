# Configurações de execução vindas do app.py
# Este arquivo é gerado automaticamente pelo app.py

CATEGORIA_WP = "Others"
STATUS_PUBLICACAO = "draft"  # 'draft' ou 'publish'
QUANTIDADE_TEXTOS = 1
TOPICOS_LISTA = ["Tecnologia 2025"]
AUTHOR_ID = 1

def get_configuracoes_execucao():
    return {
        'categoria_wp': CATEGORIA_WP,
        'status_publicacao': STATUS_PUBLICACAO,
        'quantidade_textos': QUANTIDADE_TEXTOS,
        'topicos_lista': TOPICOS_LISTA,
        'author_id': AUTHOR_ID
    }

def set_configuracoes_execucao(categoria_wp="Others", status_publicacao="draft", quantidade_textos=3, topicos_lista=None, author_id=1):
    global CATEGORIA_WP, STATUS_PUBLICACAO, QUANTIDADE_TEXTOS, TOPICOS_LISTA, AUTHOR_ID
    CATEGORIA_WP = categoria_wp
    STATUS_PUBLICACAO = status_publicacao
    QUANTIDADE_TEXTOS = quantidade_textos
    AUTHOR_ID = author_id
    if topicos_lista:
        TOPICOS_LISTA = topicos_lista
