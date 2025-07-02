#!/bin/bash

# Deploy do RoboWordpress
echo "🚀 RoboWordpress - Script de Deploy"
echo "===================================="

# Verificar se está em um repositório git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Este não é um repositório Git!"
    exit 1
fi

# Verificar se há mudanças não commitadas
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Há mudanças não commitadas. Fazendo commit..."
    git add .
    git commit -m "Deploy: Updates before deployment"
fi

echo "📋 Escolha o tipo de deploy:"
echo "1. 🌐 Streamlit Cloud (Recomendado)"
echo "2. 🐳 Docker Local"
echo "3. ☁️  Heroku"
echo "4. 📤 Apenas push para GitHub"

read -p "Digite sua escolha (1-4): " choice

case $choice in
    1)
        echo "🌐 Deploy no Streamlit Cloud"
        echo "1. Faça push para GitHub (será feito automaticamente)"
        echo "2. Acesse: https://streamlit.io/cloud"
        echo "3. Conecte seu repositório GitHub"
        echo "4. Configure as secrets conforme WEB_DEPLOY.md"
        
        # Push para GitHub
        echo "📤 Fazendo push para GitHub..."
        git push origin main
        
        echo "✅ Pronto! Configure o Streamlit Cloud agora."
        echo "📋 URL do repositório: $(git config --get remote.origin.url)"
        ;;
        
    2)
        echo "🐳 Deploy Docker Local"
        
        # Verificar se Docker está instalado
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker não está instalado!"
            exit 1
        fi
        
        # Verificar se .env existe
        if [ ! -f .env ]; then
            echo "❌ Arquivo .env não encontrado!"
            echo "📋 Copie .env.example para .env e configure suas credenciais"
            exit 1
        fi
        
        echo "🔨 Construindo imagem Docker..."
        docker build -t robowordpress .
        
        echo "🚀 Iniciando container..."
        docker-compose up -d
        
        echo "✅ RoboWordpress rodando em: http://localhost:8501"
        echo "📊 Para ver logs: docker-compose logs -f"
        echo "🛑 Para parar: docker-compose down"
        ;;
        
    3)
        echo "☁️  Deploy no Heroku"
        
        # Verificar se Heroku CLI está instalado
        if ! command -v heroku &> /dev/null; then
            echo "❌ Heroku CLI não está instalado!"
            echo "📥 Instale em: https://devcenter.heroku.com/articles/heroku-cli"
            exit 1
        fi
        
        # Verificar se está logado no Heroku
        if ! heroku auth:whoami &> /dev/null; then
            echo "🔑 Faça login no Heroku:"
            heroku auth:login
        fi
        
        read -p "📝 Nome da app no Heroku: " app_name
        
        echo "🏗️  Criando app no Heroku..."
        heroku create $app_name
        
        echo "⚙️  Configurando variáveis de ambiente..."
        echo "📋 Configure manualmente no painel do Heroku ou use:"
        echo "heroku config:set WP_URL=\"https://seu-site.com\" -a $app_name"
        echo "heroku config:set WP_USER=\"usuario\" -a $app_name"
        echo "# ... outras variáveis"
        
        echo "📤 Fazendo deploy..."
        git push heroku main
        
        echo "✅ Deploy concluído!"
        echo "🌐 URL: https://$app_name.herokuapp.com"
        ;;
        
    4)
        echo "📤 Push para GitHub"
        git push origin main
        echo "✅ Push concluído!"
        echo "📋 Agora configure o deploy manual conforme WEB_DEPLOY.md"
        ;;
        
    *)
        echo "❌ Opção inválida!"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deploy finalizado!"
echo "📖 Para mais informações, consulte WEB_DEPLOY.md"
