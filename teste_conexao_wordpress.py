#!/usr/bin/env python3
"""
Teste de Conexão WordPress
Baseado no robo_pilloto.py
"""

import requests
import time
from requests.auth import HTTPBasicAuth
import json
from config import *

# Validar configurações ao iniciar
if not validar_configuracoes():
    exit(1)

def testar_conexao_basica():
    """Testa conexão básica com a API do WordPress"""
    print("1. Testando conexão básica com WordPress...")
    try:
        # Endpoint simples para testar conectividade
        response = requests.get(f"{WP_URL}/wp-json/wp/v2", timeout=10)
        response.raise_for_status()
        print(f"   ✅ WordPress acessível - Status: {response.status_code}")
        return True
    except Exception as e:
        print(f"   ❌ Erro na conexão básica: {e}")
        return False

def testar_autenticacao():
    """Testa autenticação com credenciais"""
    print("2. Testando autenticação...")
    try:
        # Testar endpoint que requer autenticação
        categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
        response = requests.get(categories_endpoint, auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), timeout=10)
        response.raise_for_status()
        
        categories = response.json()
        print(f"   ✅ Autenticação OK - {len(categories)} categorias encontradas")
        
        # Mostrar algumas categorias
        print("   Categorias disponíveis:")
        for cat in categories[:5]:  # Mostrar apenas as primeiras 5
            print(f"     - {cat['name']} (ID: {cat['id']})")
        
        return True, categories
    except Exception as e:
        print(f"   ❌ Erro na autenticação: {e}")
        return False, []

def testar_categoria_others(categories):
    """Testa se a categoria 'Others' existe ou cria uma nova"""
    print("3. Verificando categoria 'Others'...")
    try:
        # Procurar categoria Others
        others_category_id = None
        for category in categories:
            if category['name'].lower() == 'others':
                others_category_id = category['id']
                break
        
        if others_category_id:
            print(f"   ✅ Categoria 'Others' encontrada - ID: {others_category_id}")
            return others_category_id
        else:
            print("   ⚠️  Categoria 'Others' não encontrada. Tentando criar...")
            
            # Criar categoria Others
            categories_endpoint = f"{WP_URL}/wp-json/wp/v2/categories"
            create_data = {
                'name': 'Others',
                'slug': 'others',
                'description': 'Categoria criada automaticamente pelo robô'
            }
            
            response = requests.post(
                categories_endpoint, 
                json=create_data, 
                auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), 
                timeout=10
            )
            response.raise_for_status()
            
            new_category = response.json()
            print(f"   ✅ Categoria 'Others' criada - ID: {new_category['id']}")
            return new_category['id']
            
    except Exception as e:
        print(f"   ❌ Erro ao gerenciar categoria 'Others': {e}")
        print("   📝 Usando categoria padrão (ID: 1)")
        return 1

def testar_criacao_post_rascunho(category_id):
    """Testa criação de um post de rascunho"""
    print("4. Testando criação de post rascunho...")
    try:
        # Dados do post de teste
        post_data = {
            'title': '[TESTE CONEXÃO] Post de Teste - ' + time.strftime("%Y-%m-%d %H:%M:%S"),
            'content': '''
            <h2>Este é um post de teste</h2>
            <p>Este post foi criado automaticamente pelo script de teste de conexão do WordPress.</p>
            <h3>Detalhes do Teste:</h3>
            <ul>
                <li>Data/Hora: ''' + time.strftime("%d/%m/%Y às %H:%M:%S") + '''</li>
                <li>Script: teste_conexao_wordpress.py</li>
                <li>Status: Rascunho (não publicado)</li>
            </ul>
            <p><strong>Este post pode ser excluído com segurança.</strong></p>
            ''',
            'status': 'draft',  # Rascunho
            'categories': [category_id],
            'excerpt': 'Post de teste criado automaticamente para verificar conexão com WordPress.'
        }
        
        # Enviar para WordPress
        posts_endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        response = requests.post(
            posts_endpoint, 
            json=post_data, 
            auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), 
            timeout=20
        )
        response.raise_for_status()
        
        post_info = response.json()
        print(f"   ✅ Post rascunho criado com sucesso!")
        print(f"     - ID: {post_info['id']}")
        print(f"     - Título: {post_info['title']['rendered']}")
        print(f"     - Status: {post_info['status']}")
        print(f"     - URL Admin: {WP_URL}/wp-admin/post.php?post={post_info['id']}&action=edit")
        
        return True, post_info['id']
        
    except Exception as e:
        print(f"   ❌ Erro ao criar post: {e}")
        if hasattr(e, 'response') and e.response:
            try:
                error_detail = e.response.json()
                print(f"     Detalhes do erro: {error_detail}")
            except:
                print(f"     Resposta HTTP: {e.response.text[:200]}...")
        return False, None

def testar_listagem_posts():
    """Testa listagem de posts recentes"""
    print("5. Testando listagem de posts...")
    try:
        posts_endpoint = f"{WP_URL}/wp-json/wp/v2/posts"
        params = {
            'per_page': 5,  # Apenas os 5 mais recentes
            'status': 'draft,publish'  # Rascunhos e publicados
        }
        
        response = requests.get(
            posts_endpoint, 
            params=params,
            auth=HTTPBasicAuth(WP_USER, WP_PASSWORD), 
            timeout=10
        )
        response.raise_for_status()
        
        posts = response.json()
        print(f"   ✅ Listagem OK - {len(posts)} posts encontrados")
        
        print("   Posts recentes:")
        for post in posts:
            status_emoji = "📝" if post['status'] == 'draft' else "✅"
            print(f"     {status_emoji} {post['title']['rendered'][:50]}... (ID: {post['id']})")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao listar posts: {e}")
        return False

def executar_todos_os_testes():
    """Executa todos os testes de conexão"""
    print("="*60)
    print("TESTE DE CONEXÃO WORDPRESS")
    print("Baseado no robo_pilloto.py")
    print("="*60)
    print()
    
    # Teste 1: Conexão básica
    if not testar_conexao_basica():
        print("\n❌ FALHA: Não foi possível conectar ao WordPress.")
        print("Verifique se a URL está correta e se o site está online.")
        return False
    
    print()
    
    # Teste 2: Autenticação
    auth_ok, categories = testar_autenticacao()
    if not auth_ok:
        print("\n❌ FALHA: Problema na autenticação.")
        print("Verifique as credenciais WP_USER e WP_PASSWORD.")
        return False
    
    print()
    
    # Teste 3: Categoria Others
    category_id = testar_categoria_others(categories)
    
    print()
    
    # Teste 4: Criação de post
    post_ok, post_id = testar_criacao_post_rascunho(category_id)
    if not post_ok:
        print("\n❌ FALHA: Não foi possível criar post de teste.")
        return False
    
    print()
    
    # Teste 5: Listagem
    if not testar_listagem_posts():
        print("\n⚠️  AVISO: Problema na listagem de posts.")
    
    print()
    print("="*60)
    print("✅ TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print("="*60)
    print()
    print("RESUMO:")
    print(f"✅ WordPress acessível em: {WP_URL}")
    print(f"✅ Autenticação funcionando para usuário: {WP_USER}")
    print(f"✅ Categoria 'Others' disponível (ID: {category_id})")
    if post_id:
        print(f"✅ Post de teste criado (ID: {post_id})")
    print()
    print("🚀 O robô piloto deve funcionar corretamente!")
    print()
    print("📝 PRÓXIMOS PASSOS:")
    print("- Execute o robo_pilloto.py para gerar conteúdo real")
    print("- Verifique os rascunhos no WordPress Admin")
    print("- Configure os tópicos no Google Sheets se necessário")
    
    return True

if __name__ == "__main__":
    try:
        executar_todos_os_testes()
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário.")
    except Exception as e:
        print(f"\n\n❌ ERRO INESPERADO: {e}")
        print("Verifique suas configurações e tente novamente.")
