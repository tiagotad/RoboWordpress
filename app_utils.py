"""
Utilitários para o aplicativo RoboWordpress
"""
import requests
from requests.auth import HTTPBasicAuth

def buscar_autores_wordpress(wp_url, wp_user, wp_password):
    """
    Busca lista de autores do WordPress via API REST
    
    Args:
        wp_url (str): URL do site WordPress
        wp_user (str): Usuário do WordPress
        wp_password (str): Senha/Application Password do WordPress
    
    Returns:
        list: Lista de tuplas (id, nome) dos autores
    """
    try:
        # URL da API para buscar usuários/autores
        api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/users"
        
        print(f"[DEBUG] Buscando autores em: {api_url}")
        print(f"[DEBUG] Usuário: {wp_user}")
        
        # Tentar diferentes parâmetros para maximizar chances de sucesso
        params_list = [
            {'per_page': 100, 'context': 'view'},  # Parâmetros padrão
            {'per_page': 100},  # Sem context
            {'per_page': 50, 'context': 'view'},   # Menos usuários
            {'per_page': 20},   # Ainda menos
            {}  # Parâmetros mínimos
        ]
        
        for i, params in enumerate(params_list):
            print(f"[DEBUG] Tentativa {i+1} com parâmetros: {params}")
            
            # Fazer requisição com autenticação
            response = requests.get(
                api_url,
                auth=HTTPBasicAuth(wp_user, wp_password),
                timeout=15,
                params=params
            )
            
            print(f"[DEBUG] Status da resposta (tentativa {i+1}): {response.status_code}")
            
            if response.status_code == 200:
                usuarios = response.json()
                print(f"[DEBUG] Encontrados {len(usuarios)} usuários na tentativa {i+1}")
                
                # Retornar lista de (id, nome) dos autores
                autores = []
                for user in usuarios:
                    user_id = user.get('id')
                    user_name = user.get('name', 'Nome não disponível')
                    user_slug = user.get('slug', '')
                    if user_id:
                        # Mostrar nome e slug para melhor identificação
                        display_name = f"{user_name}" + (f" ({user_slug})" if user_slug and user_slug != user_name.lower().replace(' ', '') else "")
                        autores.append((user_id, display_name))
                        print(f"[DEBUG] Autor: {user_id} - {display_name}")
                
                return autores
                
            elif response.status_code == 401:
                print(f"[ERRO] Não autorizado (401) na tentativa {i+1}")
                if i == len(params_list) - 1:  # Última tentativa
                    print(f"[INFO] Todas as tentativas falharam com 401 - usuário pode não ter permissão")
                continue
                
            elif response.status_code == 403:
                print(f"[ERRO] Acesso negado (403) na tentativa {i+1}")
                if i == len(params_list) - 1:  # Última tentativa
                    print(f"[INFO] Todas as tentativas falharam com 403 - permissões insuficientes")
                continue
                
            else:
                print(f"[ERRO] Falha na tentativa {i+1}: {response.status_code}")
                print(f"[ERRO] Resposta: {response.text[:200]}")
                if i == len(params_list) - 1:  # Última tentativa
                    print(f"[INFO] Todas as tentativas falharam")
        
        # Se chegou aqui, todas as tentativas falharam
        return []
            
    except requests.exceptions.Timeout:
        print(f"[ERRO] Timeout ao conectar com WordPress")
        return []
    except requests.exceptions.ConnectionError:
        print(f"[ERRO] Erro de conexão com WordPress")
        return []
    except Exception as e:
        print(f"[ERRO] Erro ao conectar com WordPress: {e}")
        return []

def validar_conexao_wordpress(wp_url, wp_user, wp_password):
    """
    Valida se a conexão com WordPress está funcionando
    
    Args:
        wp_url (str): URL do site WordPress
        wp_user (str): Usuário do WordPress
        wp_password (str): Senha/Application Password do WordPress
    
    Returns:
        bool: True se conexão OK, False caso contrário
    """
    try:
        # Testar conexão básica com a API
        api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/posts"
        
        response = requests.get(
            api_url,
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10,
            params={'per_page': 1}  # Buscar apenas 1 post para teste
        )
        
        return response.status_code in [200, 401]  # 401 também indica que a API está acessível
        
    except Exception as e:
        print(f"[ERRO] Erro na validação: {e}")
        return False

def buscar_categorias_wordpress(wp_url, wp_user, wp_password):
    """
    Busca lista de categorias do WordPress via API REST
    
    Args:
        wp_url (str): URL do site WordPress
        wp_user (str): Usuário do WordPress
        wp_password (str): Senha/Application Password do WordPress
    
    Returns:
        list: Lista de tuplas (id, nome) das categorias
    """
    try:
        # URL da API para buscar categorias
        api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/categories"
        
        print(f"[DEBUG] Buscando categorias em: {api_url}")
        
        # Fazer requisição com autenticação
        response = requests.get(
            api_url,
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=15,
            params={'per_page': 100}  # Buscar até 100 categorias
        )
        
        print(f"[DEBUG] Status da resposta (categorias): {response.status_code}")
        
        if response.status_code == 200:
            categorias = response.json()
            print(f"[DEBUG] Encontradas {len(categorias)} categorias")
            
            # Extrair ID e nome das categorias
            lista_categorias = []
            for categoria in categorias:
                cat_id = categoria.get('id')
                cat_name = categoria.get('name', 'Nome não disponível')
                if cat_id and cat_name:
                    lista_categorias.append((cat_id, cat_name))
                    print(f"[DEBUG] Categoria: {cat_id} - {cat_name}")
            
            # Verificar se categoria 32174 (mundo) existe
            categoria_mundo = next((cat for cat in lista_categorias if cat[0] == 32174), None)
            if categoria_mundo:
                print(f"[DEBUG] ✅ Categoria padrão (32174 - mundo) encontrada: {categoria_mundo[1]}")
            else:
                print(f"[DEBUG] ⚠️ Categoria padrão (32174 - mundo) não encontrada")
                # Adicionar manualmente se não existir (pode não estar na primeira página)
                lista_categorias.insert(0, (32174, "mundo (ID: 32174)"))
                print(f"[DEBUG] ✅ Categoria padrão adicionada manualmente")
            
            # Adicionar outras categorias padrão se necessário
            categorias_padrao = [
                (1, "Uncategorized"),
                (0, "Others")  # ID 0 como fallback
            ]
            
            for cat_id, cat_name in categorias_padrao:
                if not any(cat[0] == cat_id for cat in lista_categorias):
                    lista_categorias.append((cat_id, cat_name))
            
            return lista_categorias
        else:
            print(f"[ERRO] Falha ao buscar categorias: {response.status_code}")
            print(f"[ERRO] Resposta: {response.text[:200]}")
            # Retornar categoria padrão em caso de erro
            return [(32174, "mundo (ID: 32174)"), (1, "Uncategorized"), (0, "Others")]
            
    except Exception as e:
        print(f"[ERRO] Erro ao conectar com WordPress para buscar categorias: {e}")
        # Retornar categoria padrão em caso de erro
        return [(32174, "mundo (ID: 32174)"), (1, "Uncategorized"), (0, "Others")]

def buscar_usuario_atual(wp_url, wp_user, wp_password):
    """
    Busca informações do usuário logado (sempre funciona se as credenciais estão corretas)
    
    Args:
        wp_url (str): URL do site WordPress
        wp_user (str): Usuário do WordPress
        wp_password (str): Senha/Application Password do WordPress
    
    Returns:
        tuple: (id, nome) do usuário atual ou None se erro
    """
    try:
        # URL da API para buscar o usuário atual
        api_url = f"{wp_url.rstrip('/')}/wp-json/wp/v2/users/me"
        
        print(f"[DEBUG] Buscando usuário atual em: {api_url}")
        
        # Fazer requisição com autenticação
        response = requests.get(
            api_url,
            auth=HTTPBasicAuth(wp_user, wp_password),
            timeout=10
        )
        
        print(f"[DEBUG] Status da resposta (usuário atual): {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data.get('id')
            user_name = user_data.get('name', 'Usuário atual')
            print(f"[DEBUG] Usuário atual: {user_id} - {user_name}")
            return (user_id, user_name)
        else:
            print(f"[ERRO] Falha ao buscar usuário atual: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"[ERRO] Erro ao buscar usuário atual: {e}")
        return None
