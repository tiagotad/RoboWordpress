# 🚀 COMO PUBLICAR NO STREAMLIT CLOUD

## 🌐 Deploy Automático na Web

### 📋 Pré-requisitos Necessários:

1. **Repositório GitHub** (✅ Já criado!)
2. **Conta Streamlit Cloud** (gratuita)

### 🛠️ Passos para Publicar:

#### 1. **Acesse o Streamlit Cloud**
- Vá para: https://streamlit.io/cloud
- Clique em **"Sign up"** ou **"Log in"**
- Use sua conta GitHub para entrar

#### 2. **Criar Nova App**
- Clique em **"New app"**
- Selecione **"From existing repo"**

#### 3. **Configurar Repositório**
- **Repository:** `tiagotad/RoboWordpress`
- **Branch:** `main`
- **Main file path:** `app.py`
- **App name:** `robowordpress` (ou outro nome)

#### 4. **⚙️ CONFIGURAR SECRETS (IMPORTANTE!)**

No painel do Streamlit, vá em **Settings > Secrets** e adicione:

```toml
# Cole exatamente assim no campo Secrets:

WP_URL = "https://seu-site-wordpress.com"
WP_USER = "seu-usuario-wordpress"
WP_PASSWORD = "sua-senha-wordpress"
OPENAI_API_KEY = "sk-sua-chave-openai"
GOOGLE_SHEET_ID = "1abc123-sua-planilha-id"
GOOGLE_SHEET_NAME = "Nome da Sua Planilha"
CREDENTIALS_FILE = "credenciais_google.json"
```

#### 5. **📁 Credenciais Google (IMPORTANTE!)**

**Método 1 - GitHub Secrets (Recomendado):**
1. No GitHub, vá em **Settings > Secrets and variables > Actions**
2. Clique **"New repository secret"**
3. Nome: `GOOGLE_CREDENTIALS_JSON`
4. Value: Cole todo o conteúdo do arquivo `credenciais_google.json`

**Método 2 - Upload Direto:**
1. Adicione o arquivo `credenciais_google.json` ao repositório
2. ⚠️ **ATENÇÃO:** Configure `.gitignore` para não expor credenciais

#### 6. **🚀 Deploy**
- Clique em **"Deploy!"**
- Aguarde alguns minutos
- ✅ **Pronto! Sua app estará online 24/7**

### 🌐 **URL Final:**
Sua interface estará disponível em:
`https://robowordpress.streamlit.app`

### 🎯 **Como Usar Após Deploy:**

1. **Acesse a URL** da sua app
2. **Configure credenciais** (se ainda não fez)
3. **Use o editor de prompts** na interface
4. **Execute robôs** com um clique
5. **Monitore resultados** em tempo real

### 🔧 **Atualizações:**

Para atualizar a app:
1. Faça mudanças no código local
2. `git add .`
3. `git commit -m "Sua mensagem"`
4. `git push origin main`
5. ✅ **Streamlit atualizará automaticamente!**

### 🛠️ **Solução de Problemas:**

**App não carrega:**
- Verifique se todas as secrets estão configuradas
- Confirme se o arquivo `requirements.txt` está correto
- Veja os logs no painel do Streamlit Cloud

**Erro de credenciais:**
- Confirme se as variáveis estão corretas no Secrets
- Verifique se o arquivo Google Credentials está acessível

**Erro de dependências:**
- Verifique o arquivo `requirements.txt`
- Certifique-se de que todas as versões são compatíveis

### 📞 **Suporte:**

Se precisar de ajuda:
1. Verifique os logs no Streamlit Cloud
2. Teste localmente primeiro: `streamlit run app.py`
3. Consulte: https://docs.streamlit.io/streamlit-cloud

---

🎉 **Pronto! Seu RoboWordpress estará online e acessível 24/7!**

**🌐 Acesso Web:** https://robowordpress.streamlit.app
**🔗 Repositório:** https://github.com/tiagotad/RoboWordpress
