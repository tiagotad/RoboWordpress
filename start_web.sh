#!/bin/bash

echo "🚀 Iniciando RoboWordpress Web Interface..."
echo ""

# Verificar se está no diretório correto
if [ ! -f "app.py" ]; then
    echo "❌ Erro: Execute este script na pasta do projeto RoboWordpress"
    exit 1
fi

# Verificar ambiente virtual
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python -m venv venv
fi

# Ativar ambiente virtual e instalar dependências
echo "📦 Instalando/Atualizando dependências..."
source venv/bin/activate
pip install -r requirements.txt

# Verificar configurações
echo "🔧 Verificando configurações..."
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado. Criando..."
    cp .env.example .env
    echo "✅ Arquivo .env criado. IMPORTANTE: Configure suas credenciais!"
fi

if [ ! -f "config.py" ]; then
    echo "⚠️  Arquivo config.py não encontrado. Criando..."
    cp config_template.py config.py
    echo "✅ Arquivo config.py criado."
fi

echo ""
echo "🎉 Tudo pronto!"
echo ""
echo "🌐 Abrindo interface web..."
echo "📋 Instruções:"
echo "   - A interface abrirá automaticamente no navegador"
echo "   - URL: http://localhost:8501"
echo "   - Para parar: Ctrl+C"
echo ""
echo "⚠️  IMPORTANTE: Configure suas credenciais no arquivo .env antes de usar!"
echo ""

# Iniciar Streamlit
streamlit run app.py --server.port 8501 --server.address localhost
