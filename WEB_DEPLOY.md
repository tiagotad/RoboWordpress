# 🚀 Deploy do RoboWordpress na Web

## 📋 Opções de Deploy

### 1. 🌐 Streamlit Cloud (Recomendado - Gratuito)

O **Streamlit Cloud** é a forma mais fácil de publicar a interface web do RoboWordpress.

#### 📋 Pré-requisitos:
- Repositório GitHub público
- Conta no [Streamlit Cloud](https://streamlit.io/cloud)

#### 🛠️ Passos para Deploy:

1. **Acesse:** https://streamlit.io/cloud
2. **Faça login** com sua conta GitHub
3. **Clique em "New app"**
4. **Configure:**
   - Repository: `seu-usuario/RoboWordpress`
   - Branch: `main`
   - Main file path: `app.py`
5. **Clique em "Deploy!"**

#### ⚙️ Configuração de Secrets:

No painel do Streamlit Cloud, configure as **secrets** em `Settings > Secrets`:

```toml
# Secrets do Streamlit Cloud
[secrets]
WP_URL = "https://seu-site.com"
WP_USER = "seu-usuario"
WP_PASSWORD = "sua-senha"
OPENAI_API_KEY = "sk-..."
GOOGLE_SHEET_ID = "1abc..."
GOOGLE_SHEET_NAME = "Nome da Planilha"
```

#### 📁 Upload de Credenciais Google:

1. No repositório GitHub, adicione o arquivo `credenciais_google.json` (criptografado)
2. Ou use GitHub Secrets para armazenar o conteúdo do JSON

### 2. 🐳 Deploy com Docker

#### Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build e Run:
```bash
docker build -t robowordpress .
docker run -p 8501:8501 robowordpress
```

### 3. 🌍 Heroku

#### Arquivos necessários:

**Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt:**
```
python-3.11.2
```

#### Deploy:
```bash
heroku create robowordpress-app
heroku config:set WP_URL="https://seu-site.com"
heroku config:set WP_USER="usuario"
heroku config:set WP_PASSWORD="senha"
heroku config:set OPENAI_API_KEY="sk-..."
heroku config:set GOOGLE_SHEET_ID="1abc..."
git push heroku main
```

### 4. ☁️ AWS/GCP/Azure

Para deploy em cloud providers, use:
- **AWS**: Elastic Beanstalk ou ECS
- **GCP**: Cloud Run ou App Engine
- **Azure**: Container Instances ou App Service

## 🔐 Segurança

### Variáveis de Ambiente:
- ✅ Nunca commite credenciais no código
- ✅ Use secrets/environment variables
- ✅ Configure HTTPS em produção

### Acesso:
- 🔒 Configure autenticação se necessário
- 🛡️ Use firewall para restringir acesso
- 📊 Monitor logs de acesso

## 🎯 Uso por Estagiários

Após o deploy:

1. **Acesse a URL** do app deployado
2. **Use a interface** normalmente
3. **Edite prompts** na interface visual
4. **Execute robôs** com um clique

## 📞 Suporte

Para problemas no deploy:
1. Verifique logs no painel do serviço
2. Confirme se todas as variáveis estão configuradas
3. Teste localmente primeiro: `streamlit run app.py`

---

🎉 **Pronto! O RoboWordpress estará disponível 24/7 na web!**
