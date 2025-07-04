# Configurações de execução vindas do app.py
# Este arquivo é gerado automaticamente pelo app.py

CATEGORIA_WP = "Others"
STATUS_PUBLICACAO = "draft"  # 'draft' ou 'publish'
QUANTIDADE_TEXTOS = 1
TOPICOS_LISTA = ["Teste de Interface"]
AUTHOR_ID = 71

# Credenciais WordPress da interface
WP_URL = "https://www.elhombre.com.br"
WP_USER = "eutiago"
WP_PASSWORD = "oJrD 8N3S 7SPp 0Zcz q1vz o0Gd"

def get_configuracoes_execucao():
    return {
        'categoria_wp': CATEGORIA_WP,
        'status_publicacao': STATUS_PUBLICACAO,
        'quantidade_textos': QUANTIDADE_TEXTOS,
        'topicos_lista': TOPICOS_LISTA,
        'author_id': AUTHOR_ID,
        'wp_url': WP_URL,
        'wp_user': WP_USER,
        'wp_password': WP_PASSWORD
    }

