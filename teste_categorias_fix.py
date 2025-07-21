#!/usr/bin/env python3
"""
Teste das categorias WordPress após correções
"""

# Simular config_execucao.py gerado
topicos_teste = ['Filmes e Cinema', 'Séries de TV']
quantidade_textos = 2
categoria_id = 32174

# Testar geração de config
topicos_expandidos = []
for topico in topicos_teste:
    topicos_expandidos.extend([topico] * int(quantidade_textos))

topicos_repr = repr(topicos_expandidos)

print("=== TESTE DAS CORREÇÕES ===")
print(f"Tópicos originais: {topicos_teste}")
print(f"Quantidade por tópico: {quantidade_textos}")
print(f"Tópicos expandidos: {topicos_expandidos}")
print(f"Representação Python: {topicos_repr}")
print(f"Categoria ID: {categoria_id}")

# Simular código gerado
config_codigo = f"""
STATUS_PUBLICACAO = "draft"
QUANTIDADE_TEXTOS = {quantidade_textos}
TOPICOS_LISTA = {topicos_repr}
AUTHOR_ID = 210
CATEGORIA_ID = {categoria_id}
"""

print("\n=== CÓDIGO GERADO ===")
print(config_codigo)

# Testar se pode ser executado
try:
    exec(config_codigo)
    print("✅ Código gerado é válido!")
    print(f"✅ TOPICOS_LISTA carregou: {len(TOPICOS_LISTA)} itens")
    print(f"✅ CATEGORIA_ID: {CATEGORIA_ID}")
except Exception as e:
    print(f"❌ Erro no código gerado: {e}")

print("\n=== SIMULAÇÃO config.get() ===")
config_sim = {
    'categoria_id': categoria_id,
    'status_publicacao': 'draft',
    'author_id': 210
}

# Simular como o robô vai usar
post_data = {
    'title': "Teste",
    'content': "Conteúdo teste",
    'status': config_sim.get('status_publicacao', 'draft'),
    'categories': [config_sim.get('categoria_id', 1)],  # Nova forma correta
    'author': config_sim.get('author_id', 1)
}

print(f"✅ Dados do post: {post_data}")
print("✅ Categoria corretamente configurada!")
