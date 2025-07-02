# 🔧 COMO CONFIGURAR CREDENCIAIS NO STREAMLIT CLOUD

## 📋 **PROBLEMA:** App pede credenciais mas não consegue configurar

### 🛠️ **SOLUÇÃO PASSO A PASSO:**

## 1. 🌐 **Acesse Seu App no Streamlit Cloud**

1. Vá para: https://share.streamlit.io/
2. Faça login com sua conta GitHub
3. Encontre seu app **RoboWordpress** na lista

## 2. ⚙️ **Acessar Configurações**

1. **Clique no seu app** RoboWordpress
2. **Clique no menu "⋮" (três pontos)** no canto superior direito
3. **Selecione "Settings"**

## 3. 🔐 **Configurar Secrets (CREDENCIAIS)**

1. **Na página de Settings, clique na aba "Secrets"**
2. **No campo de texto grande, cole EXATAMENTE isso:**

```toml
# Cole EXATAMENTE este texto (substitua pelos seus valores):

WP_URL = "https://seu-site-wordpress.com"
WP_USER = "seu_usuario_wordpress"
WP_PASSWORD = "sua_senha_wordpress"
OPENAI_API_KEY = "sk-proj-abcd1234..."
GOOGLE_SHEET_ID = "1AbCdEfG234567890HiJkLmNoPqRsTuVwXyZ"
GOOGLE_SHEET_NAME = "Nome da Sua Planilha"
CREDENTIALS_FILE = "credenciais_google.json"
```

3. **Clique "Save"**

## 4. 📁 **Configurar Credenciais Google (IMPORTANTE!)**

### **Método Simples - Upload Direto:**

1. **No seu computador**, abra o arquivo `credenciais_google.json`
2. **Copie TODO o conteúdo** do arquivo
3. **No Streamlit Cloud**, adicione na seção Secrets:

```toml
# Adicione esta linha nas suas secrets:
GOOGLE_CREDENTIALS = '''
{
  "type": "service_account",
  "project_id": "seu-projeto",
  "private_key_id": "abcd1234...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_AQUI\n-----END PRIVATE KEY-----\n",
  "client_email": "seu-service@projeto.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/seu-service%40projeto.iam.gserviceaccount.com"
}
'''
```

## 5. 🔄 **Reiniciar o App**

1. **Salve as secrets**
2. **Volte para seu app**
3. **Clique "Reboot"** (reiniciar)
4. **Aguarde alguns segundos**

## 6. ✅ **Verificar se Funcionou**

1. **Acesse seu app**
2. **Vá na seção "⚙️ Configuração"**
3. **Deve mostrar status verde** para todas as credenciais

---

## 🚨 **SE AINDA NÃO FUNCIONAR:**

### **Opção A - Verificar Formato das Secrets:**

Certifique-se que o formato está EXATAMENTE assim:
```toml
WP_URL = "https://seusite.com"
WP_USER = "usuario"
# SEM espaços extras, COM aspas
```

### **Opção B - Usar Interface Simplificada:**

Se o problema persistir, vou criar uma versão que não precisa do Google Sheets inicialmente.

## 📞 **PRECISA DE AJUDA?**

Me diga:
1. Qual erro específico aparece?
2. Você conseguiu acessar a seção "Settings > Secrets"?
3. As credenciais foram salvas com sucesso?

## 🎯 **EXEMPLO COMPLETO DE SECRETS:**

```toml
WP_URL = "https://meusite.wordpress.com"
WP_USER = "admin"
WP_PASSWORD = "MinhaSenh@123"
OPENAI_API_KEY = "sk-proj-AbCd1234..."
GOOGLE_SHEET_ID = "1ABC123DEF456GHI789JKL"
GOOGLE_SHEET_NAME = "Blog Topics"
CREDENTIALS_FILE = "credenciais_google.json"
```

**🔧 Siga estes passos e seu app funcionará perfeitamente!**
