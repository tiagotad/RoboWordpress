#!/bin/bash
# Script para executar o teste de conexão WordPress

echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

echo "📝 Executando teste de conexão WordPress..."
python teste_conexao_wordpress.py

echo "✅ Teste concluído!"
