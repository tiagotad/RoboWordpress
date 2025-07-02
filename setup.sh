#!/bin/bash

echo "🚀 Configurando RoboWordpress..."

# 1. Criar arquivo de configuração
if [ ! -f config.py ]; then
    echo "📝 Criando config.py..."
    cp config_template.py config.py
    echo "✅ config.py criado"
else
    echo "ℹ️  config.py já existe"
fi

# 2. Criar arquivo .env
if [ ! -f .env ]; then
    echo "📝 Criando .env..."
    cp .env.example .env
    echo "✅ .env criado"
    echo ""
    echo "⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais!"
    echo "   - WP_URL, WP_USER, WP_PASSWORD"
    echo "   - OPENAI_API_KEY"
    echo "   - GOOGLE_SHEET_NAME, GOOGLE_SHEET_ID"
else
    echo "ℹ️  .env já existe"
fi

# 3. Criar ambiente virtual
if [ ! -d "venv" ]; then
    echo "🐍 Criando ambiente virtual..."
    python -m venv venv
    echo "✅ Ambiente virtual criado"
else
    echo "ℹ️  Ambiente virtual já existe"
fi

# 4. Ativar ambiente virtual e instalar dependências
echo "📦 Instalando dependências..."
source venv/bin/activate
pip install -r requirements.txt
echo "✅ Dependências instaladas"

echo ""
echo "🎉 Configuração concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Edite o arquivo .env com suas credenciais"
echo "2. Adicione o arquivo credenciais_google.json"
echo "3. Execute: source venv/bin/activate"
echo "4. Execute: python robo_pillot_v2.py"
