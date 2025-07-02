# Configurações de execução vindas do app.py
# Este arquivo é gerado automaticamente pelo app.py

# Configurações padrão
CATEGORIA_WP = "Others"
STATUS_PUBLICACAO = "draft"  # "draft" ou "publish"
QUANTIDADE_TEXTOS = 3
TOPICOS_LISTA = [
    "Filmes e Cinema",
    "Séries de TV",
    "História e Curiosidades",
    "Viagem e Turismo",
    "Livros e Literatura"
]

def get_configuracoes_execucao():
    """Retorna as configurações de execução"""
    return {
        'categoria_wp': CATEGORIA_WP,
        'status_publicacao': STATUS_PUBLICACAO,
        'quantidade_textos': QUANTIDADE_TEXTOS,
        'topicos_lista': TOPICOS_LISTA
    }

def set_configuracoes_execucao(categoria_wp="Others", status_publicacao="draft", quantidade_textos=3, topicos_lista=None):
    """Define as configurações de execução"""
    global CATEGORIA_WP, STATUS_PUBLICACAO, QUANTIDADE_TEXTOS, TOPICOS_LISTA
    CATEGORIA_WP = categoria_wp
    STATUS_PUBLICACAO = status_publicacao
    QUANTIDADE_TEXTOS = quantidade_textos
    if topicos_lista:
        TOPICOS_LISTA = topicos_lista
