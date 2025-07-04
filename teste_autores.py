#!/usr/bin/env python3
"""
Teste específico para carregar autores do WordPress
"""

import os
import sys

# Adicionar diretório atual ao path
sys.path.append(os.getcwd())

from app_utils import buscar_autores_wordpress, buscar_categorias_wordpress, buscar_usuario_atual

def teste_autores():
    # Credenciais de exemplo (substitua pelas suas)
    wp_url = "https://www.elhombre.com.br"
    wp_user = "eutiago"
    wp_password = "oJrD 8N3S 7SPp 0Zcz q1vz o0Gd"
    
    print("🔍 TESTE DE CARREGAMENTO DE AUTORES")
    print("=" * 50)
    print(f"Site: {wp_url}")
    print(f"Usuário: {wp_user}")
    print(f"Senha: {'*' * len(wp_password)}")
    print()
    
    print("📝 Testando busca de autores...")
    autores = buscar_autores_wordpress(wp_url, wp_user, wp_password)
    
    if autores:
        print(f"✅ Sucesso! Encontrados {len(autores)} autores:")
        for autor_id, autor_nome in autores:
            print(f"  - ID: {autor_id} | Nome: {autor_nome}")
            
        # Verificar se ID 210 está na lista
        if 210 in [id for id, nome in autores]:
            print(f"🎯 ID 210 encontrado na lista!")
        else:
            print(f"⚠️ ID 210 não encontrado na lista")
    else:
        print("❌ Nenhum autor encontrado!")
        print("🔄 Tentando buscar usuário atual como fallback...")
        
        usuario_atual = buscar_usuario_atual(wp_url, wp_user, wp_password)
        if usuario_atual:
            print(f"✅ Usuário atual encontrado: ID {usuario_atual[0]} - {usuario_atual[1]}")
            print(f"💡 Na aplicação, o ID 210 será adicionado automaticamente como opção padrão")
        else:
            print("❌ Não foi possível encontrar nem mesmo o usuário atual!")
    
    print()
    print("📁 Testando busca de categorias...")
    categorias = buscar_categorias_wordpress(wp_url, wp_user, wp_password)
    
    if categorias:
        print(f"✅ Sucesso! Encontradas {len(categorias)} categorias:")
        for categoria in categorias[:10]:  # Mostrar apenas as primeiras 10
            print(f"  - {categoria}")
        if len(categorias) > 10:
            print(f"  ... e mais {len(categorias) - 10} categorias")
    else:
        print("❌ Nenhuma categoria encontrada!")

if __name__ == "__main__":
    teste_autores()
