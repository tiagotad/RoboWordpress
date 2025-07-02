#!/bin/bash
# Script simples para iniciar a interface web

echo "🚀 RoboWordpress - Iniciando Interface Web"
echo "============================================"
echo ""

# Ir para o diretório
cd /Users/tiago/Projetos/RoboWordpress

# Verificar se estamos no lugar certo
if [ ! -f "app.py" ]; then
    echo "❌ Erro: Execute este script na pasta do RoboWordpress"
    exit 1
fi

echo "📂 Diretório: $(pwd)"
echo "✅ Arquivo app.py encontrado"

# Ativar ambiente virtual
echo "🐍 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se Streamlit está instalado
if ! command -v streamlit &> /dev/null; then
    echo "📦 Instalando Streamlit..."
    pip install streamlit
fi

echo ""
echo "🌐 Iniciando servidor web..."
echo "📱 URL: http://localhost:8501"
echo "🛑 Para parar: Ctrl+C"
echo ""

# Iniciar Streamlit
streamlit run app.py --server.port 8501 --server.address localhost --server.headless false
