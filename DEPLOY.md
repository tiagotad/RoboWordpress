# 🌐 Deploy da Interface Web - RoboWordpress

## 📱 Opções de Deploy para Acesso Remoto

### 1. 🚀 **Streamlit Cloud (GRATUITO - Recomendado)**

**Vantagens:**
- ✅ Totalmente gratuito
- ✅ Deploy automático do GitHub
- ✅ SSL incluído
- ✅ Fácil de configurar

**Como fazer:**

1. **Push do código para GitHub** (já feito ✅)

2. **Acesse** https://share.streamlit.io

3. **Conecte sua conta GitHub**

4. **Deploy:**
   - Repository: `tiagotad/RoboWordpress`
   - Branch: `main`
   - Main file path: `app.py`

5. **Configure variáveis de ambiente:**
   - No painel do Streamlit Cloud, adicione as variáveis do `.env`
   - `WP_URL`, `WP_USER`, `WP_PASSWORD`, `OPENAI_API_KEY`, etc.

6. **Upload credenciais Google:**
   - No Streamlit Cloud, faça upload do `credenciais_google.json`

**URL final:** `https://seu-app.streamlit.app`

---

### 2. 🔥 **Railway (FÁCIL)**

**Vantagens:**
- ✅ Deploy simples
- ✅ $5/mês de crédito gratuito
- ✅ Conecta direto ao GitHub

**Como fazer:**

1. **Acesse** https://railway.app
2. **Conecte GitHub**
3. **Deploy from GitHub repo**
4. **Configure variáveis de ambiente**
5. **Comando de start:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

---

### 3. 🐳 **Heroku**

**Vantagens:**
- ✅ Plataforma confiável
- ✅ Dynos gratuitos limitados

**Arquivos necessários:**

1. **Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. **runtime.txt:**
```
python-3.11.0
```

---

### 4. 💻 **VPS/Servidor Próprio**

**Para usar em servidor Linux:**

1. **Instalar dependências:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx
```

2. **Clonar projeto:**
```bash
git clone https://github.com/tiagotad/RoboWordpress.git
cd RoboWordpress
```

3. **Configurar:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env com suas credenciais
```

4. **Rodar em produção:**
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

5. **Configurar Nginx (opcional)** para HTTPS

---

### 5. 🏠 **Rede Local (Para Estagiário na Empresa)**

**Opção mais simples para uso interno:**

1. **No seu computador:**
```bash
./start_web.sh
```

2. **Descobrir IP local:**
```bash
ipconfig getifaddr en0  # macOS
# ou
ip addr show | grep inet  # Linux
```

3. **Rodar com IP público da rede:**
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

4. **Estagiário acessa:**
   - `http://SEU_IP:8501`
   - Exemplo: `http://192.168.1.100:8501`

---

## 🔐 Configuração de Segurança

### Para Deploy em Produção:

1. **Variáveis de Ambiente:**
   - Nunca commite credenciais no código
   - Use o sistema de secrets da plataforma

2. **Autenticação:**
```python
# Adicionar no início do app.py
import streamlit_authenticator as stauth

# Configurar senha de acesso
if 'authenticated' not in st.session_state:
    password = st.text_input("Senha de Acesso:", type="password")
    if password == "SUA_SENHA_SEGURA":
        st.session_state['authenticated'] = True
        st.rerun()
    else:
        st.stop()
```

---

## 📋 Checklist de Deploy

### ✅ **Antes de fazer deploy:**

- [ ] ✅ Código testado localmente
- [ ] ✅ Credenciais configuradas como variáveis de ambiente
- [ ] ✅ `requirements.txt` atualizado
- [ ] ✅ Arquivo `.gitignore` protegendo credenciais
- [ ] ✅ README atualizado

### ✅ **Após deploy:**

- [ ] Testar todas as funcionalidades
- [ ] Verificar logs de erro
- [ ] Testar execução dos robôs
- [ ] Configurar monitoramento (opcional)

---

## 🎯 **Recomendação Final**

**Para o estagiário rodar quando precisar:**

1. **🥇 Melhor opção: Streamlit Cloud**
   - Grátis, confiável, fácil de usar
   - URL: `https://robowordpress-tiagotad.streamlit.app`

2. **🥈 Alternativa: Rede Local**
   - Seu computador roda o servidor
   - Estagiário acessa via IP local

3. **🥉 Opção avançada: VPS**
   - Maior controle, mas requer manutenção
