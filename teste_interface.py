#!/usr/bin/env python3
"""
Teste da nova funcionalidade de credenciais na interface
"""

# Simular entrada de credenciais
wp_url = "https://www.elhombre.com.br"
wp_user = "eutiago"
wp_password = "oJrD 8N3S 7SPp 0Zcz q1vz o0Gd"
categoria_wp = "Others"
status_publicacao = "draft"
quantidade_textos = 1
author_id = 71
topicos_lista = ["Teste de Interface"]

# Simular a geração do config_execucao.py
topicos_expandidos = []
for topico in topicos_lista:
    topicos_expandidos.extend([topico] * int(quantidade_textos))

topicos_formatados = '", "'.join(topicos_expandidos)

config_exec_code = (
    "# Configurações de execução vindas do app.py\n"
    "# Este arquivo é gerado automaticamente pelo app.py\n\n"
    f"CATEGORIA_WP = \"{categoria_wp}\"\n"
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
)

print("🧪 Testando geração de config_execucao.py com credenciais da interface...")
print("\n📄 Conteúdo gerado:")
print(config_exec_code)

# Salvar arquivo de teste
with open('config_execucao_teste.py', 'w') as f:
    f.write(config_exec_code)

print("\n✅ Arquivo config_execucao_teste.py criado!")

# Testar carregamento
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("config_execucao_teste", "config_execucao_teste.py")
    config_teste = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_teste)
    
    config = config_teste.get_configuracoes_execucao()
    print("\n🔍 Configurações carregadas:")
    for k, v in config.items():
        if 'password' in k.lower():
            print(f"  {k}: {'*' * len(str(v))}")
        else:
            print(f"  {k}: {v}")
            
    print("\n✅ Teste concluído com sucesso!")
    
except Exception as e:
    print(f"\n❌ Erro no teste: {e}")
