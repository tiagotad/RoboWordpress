#!/bin/bash

echo "🧪 Testando aplicação Streamlit..."

cd /Users/tiago/Projetos/RoboWordpress
source venv/bin/activate

echo "📱 Iniciando aplicação web em modo teste..."
echo "🌐 Acesse: http://localhost:8501"
echo "🛑 Para parar: Ctrl+C"
echo ""

streamlit run app.py --server.port 8501 --server.headless true
