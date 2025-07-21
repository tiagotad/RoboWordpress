#!/usr/bin/env python3
"""
Diagnóstico completo da API WordPress
"""

import requests
from requests.auth import HTTPBasicAuth
import json

def diagnostico_wordpress():
    print("🔍 DIAGNÓSTICO COMPLETO DA API WORDPRESS")
    print("=" * 50)
    
    # Configurações do WordPress - pegar do config_execucao.py
    try:
        from config_execucao import get_configuracoes_execucao
        config = get_configuracoes_execucao()
        wp_url = config['wp_url']
        wp_user = config['wp_user']
        wp_password = config['wp_password']
        print(f"[CONFIG] Usando configurações do config_execucao.py")
        print(f"[CONFIG] WordPress URL: {wp_url}")
        print(f"[CONFIG] WordPress User: {wp_user}")
    except Exception as e:
        print(f"[ERRO] Não foi possível carregar configurações: {e}")
        print("[AVISO] Usando configurações padrão de exemplo")
        wp_url = "https://thenextavenue.com"
        wp_user = "admin"
        wp_password = "senha_exemplo"
        
        if not all([wp_url, wp_user, wp_password]):
            print("❌ ERRO: Credenciais incompletas!")
            return False
        
        # TESTE 1: Conectividade básica
        print("🌐 TESTE 1: Conectividade com o site")
        try:
            response = requests.get(wp_url, timeout=10)
            print(f"✅ Site acessível - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Site inacessível: {e}")
            return False
        
        # TESTE 2: API REST disponível
        print("\n🔌 TESTE 2: API WordPress REST disponível")
        try:
            api_response = requests.get(f"{wp_url}/wp-json/wp/v2/", timeout=10)
            if api_response.status_code == 200:
                print("✅ API REST WordPress está ativa")
            else:
                print(f"❌ API REST não disponível - Status: {api_response.status_code}")
                print(f"📄 Resposta: {api_response.text[:200]}")
                return False
        except Exception as e:
            print(f"❌ Erro ao acessar API REST: {e}")
            return False
        
        # TESTE 3: Autenticação
        print("\n🔐 TESTE 3: Validação de autenticação")
        try:
            auth_response = requests.get(
                f'{wp_url}/wp-json/wp/v2/users/me',
                auth=HTTPBasicAuth(wp_user, wp_password),
                timeout=10
            )
            
            if auth_response.status_code == 200:
                user_data = auth_response.json()
                print(f"✅ Autenticação válida!")
                print(f"   Nome: {user_data.get('name', 'N/A')}")
                print(f"   ID: {user_data.get('id', 'N/A')}")
                print(f"   Roles: {user_data.get('roles', [])}")
            else:
                print(f"❌ Falha na autenticação - Status: {auth_response.status_code}")
                print(f"📄 Resposta: {auth_response.text[:300]}")
                return False
        except Exception as e:
            print(f"❌ Erro na autenticação: {e}")
            return False
        
        # TESTE 4: Verificar categoria
        print(f"\n📂 TESTE 4: Validação da categoria ID {categoria_id}")
        try:
            cat_response = requests.get(
                f"{wp_url}/wp-json/wp/v2/categories/{categoria_id}",
                auth=HTTPBasicAuth(wp_user, wp_password),
                timeout=10
            )
            
            if cat_response.status_code == 200:
                cat_data = cat_response.json()
                print(f"✅ Categoria válida: {cat_data.get('name')} (ID: {cat_data.get('id')})")
            else:
                print(f"⚠️ Categoria ID {categoria_id} pode não existir - Status: {cat_response.status_code}")
                print("   Usando categoria padrão (1) para teste...")
                categoria_id = 1
        except Exception as e:
            print(f"⚠️ Erro ao verificar categoria: {e}")
            categoria_id = 1
        
        # TESTE 5: Criar post de teste
        print(f"\n📝 TESTE 5: Criação de post de teste")
        
        post_data = {
            'title': 'TESTE DIAGNÓSTICO - Apagar após teste',
            'content': '<p>Este é um post de teste criado pelo diagnóstico automático. Pode ser apagado.</p>',
            'status': 'draft',  # Sempre draft para teste
            'categories': [categoria_id],
            'author': 1
        }
        
        print("📤 Enviando requisição...")
        print(f"   URL: {wp_url}/wp-json/wp/v2/posts")
        print(f"   Dados: {json.dumps(post_data, indent=2)}")
        
        try:
            headers = {'Content-Type': 'application/json'}
            post_response = requests.post(
                f'{wp_url}/wp-json/wp/v2/posts',
                json=post_data,
                auth=HTTPBasicAuth(wp_user, wp_password),
                headers=headers,
                timeout=30
            )
            
            print(f"\n📊 RESPOSTA DA API:")
            print(f"   Status Code: {post_response.status_code}")
            print(f"   Headers: {dict(post_response.headers)}")
            
            if post_response.status_code in [200, 201]:
                result = post_response.json()
                post_id = result.get('id')
                print(f"\n✅ POST CRIADO COM SUCESSO!")
                print(f"   ID: {post_id}")
                print(f"   Título: {result.get('title', {}).get('rendered', 'N/A')}")
                print(f"   Status: {result.get('status')}")
                print(f"   URL: {result.get('link', 'N/A')}")
                return True
            else:
                print(f"\n❌ FALHA AO CRIAR POST:")
                print(f"   Código: {post_response.status_code}")
                print(f"   Reason: {post_response.reason}")
                
                try:
                    error_data = post_response.json()
                    print(f"   Erro JSON:")
                    for key, value in error_data.items():
                        print(f"     {key}: {value}")
                except:
                    print(f"   Resposta texto: {post_response.text[:500]}")
                
                return False
                
        except Exception as e:
            print(f"❌ Erro na requisição: {e}")
            return False
            
    except Exception as e:
        print(f"💥 Erro geral no diagnóstico: {e}")
        return False

if __name__ == "__main__":
    print()
    sucesso = diagnostico_wordpress()
    print()
    if sucesso:
        print("🎉 DIAGNÓSTICO: API WordPress está funcionando corretamente!")
        print("   O problema pode estar no código do robô ou na chave OpenAI.")
    else:
        print("❌ DIAGNÓSTICO: Problema identificado na API WordPress.")
        print("   Corrija os problemas acima antes de usar o robô.")
    print()
