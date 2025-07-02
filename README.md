# RoboWordpress 🤖

Um robô automatizado para criação de conteúdo SEO no WordPress usando OpenAI e Google Sheets.

## 📋 Descrição

Este projeto é um sistema automatizado que:
- Lê tópicos de uma planilha do Google Sheets
- Gera conteúdo otimizado para SEO usando OpenAI
- Publica automaticamente no WordPress
- **🎯 Interface visual para edição de prompts personalizáveis**
- Inclui testes de conexão e funcionalidade

## 🚀 Funcionalidades

- ✅ **Interface Web Streamlit** - Painel de controle amigável com editor visual
- ✅ **Editor de Prompts Personalizáveis** - Controle total sobre como a IA gera conteúdo
- ✅ Integração com Google Sheets para gerenciar tópicos
- ✅ Geração automática de conteúdo usando OpenAI GPT
- ✅ Publicação automática no WordPress
- ✅ Testes de conectividade integrados
- ✅ Scripts de execução automatizada
- ✅ Deploy fácil para acesso remoto

## 📁 Estrutura do Projeto

```
RoboWordpress/
├── app.py                 # Interface web Streamlit com editor de prompts
├── robo_pilloto_v3.py     # Robô que usa prompts personalizáveis
├── robo_pillot_v2.py      # Versão principal do robô
├── robo_pilloto.py        # Versão alternativa
├── robo_simples.py        # Versão simplificada
├── prompt_manager.py      # Sistema de gerenciamento de prompts
├── prompts.json          # Arquivo de prompts personalizáveis
├── teste_conexao_wordpress.py  # Teste de conexão WordPress
├── teste_sheets.py        # Teste de conexão Google Sheets
├── teste_wordpress.py     # Testes WordPress
├── config.py             # Configurações do projeto
├── .env                  # Variáveis de ambiente (credenciais)
├── setup.sh              # Script de configuração automática
├── start_web.sh          # Script para iniciar interface web
└── requirements.txt       # Dependências Python
```

## 🛠️ Instalação

### Instalação Automática (Recomendada)

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/RoboWordpress.git
cd RoboWordpress
```

2. Execute o script de configuração:
```bash
./setup.sh
```

3. Edite o arquivo `.env` com suas credenciais:
```bash
nano .env  # ou use seu editor preferido
```

4. Adicione o arquivo de credenciais do Google:
- Baixe o arquivo JSON das credenciais da API do Google
- Renomeie para `credenciais_google.json`
- Coloque na raiz do projeto

### Instalação Manual

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USUARIO/RoboWordpress.git
cd RoboWordpress
```

2. Crie os arquivos de configuração:
```bash
cp config_template.py config.py
cp .env.example .env
```

3. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Configure suas credenciais nos arquivos `.env` e adicione `credenciais_google.json`

## 📝 Uso

### 🌐 Interface Web (Recomendada para Estagiários)

**Interface visual completa com editor de prompts:**

```bash
# Iniciar interface web
./start_web.sh

# Ou manualmente:
streamlit run app.py
```

**Acesse:** http://localhost:8501

#### 🎯 Editor de Prompts Personalizáveis

A interface inclui um **editor visual** que permite:

- ✏️  **Editar prompts** para títulos e artigos
- 🎭 **Configurar personalidade da IA** (system prompts)
- 👁️  **Preview** das mudanças antes de salvar
- 💾 **Salvar** alterações instantaneamente
- 🔄 **Restaurar** prompts padrão facilmente

#### 🤖 Robôs Disponíveis

1. **Robô Personalizável (v3)** - 🎯 Recomendado
   - Usa os prompts editados na interface
   - Totalmente customizável
   
2. **Robô Principal (v2)** - 🤖 Completo
   - Versão com todas as funcionalidades
   
3. **Robô Simples** - ⚡ Para testes
   - Versão simplificada para testes rápidos

#### 🧪 Testes Integrados

- **Teste WordPress** - Verifica conexão
- **Teste Google Sheets** - Valida planilha
- **Teste Completo** - OpenAI + WordPress

### 💻 Linha de Comando (Avançado)

#### Execução Principal
```bash
python robo_pillot_v2.py
```

#### Testes
```bash
# Teste de conexão WordPress
python teste_conexao_wordpress.py

# Teste de conexão Google Sheets
python teste_sheets.py

# Executar todos os testes
./executar_teste.sh
```

## ⚙️ Configuração

### WordPress
- URL do site
- Usuário com permissões de publicação
- Senha de aplicativo (recomendado usar Application Passwords)

### OpenAI
- Chave de API válida
- Créditos suficientes na conta

### Google Sheets
- Conta de serviço do Google Cloud
- Arquivo JSON de credenciais
- Planilha compartilhada com a conta de serviço

## 🔒 Segurança

⚠️ **IMPORTANTE**: Nunca commite credenciais no código!

- Use variáveis de ambiente para credenciais sensíveis
- Mantenha o arquivo `.env` no `.gitignore`
- Use senhas de aplicativo do WordPress quando possível
- Rotacione as chaves de API regularmente

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas:
- Abra uma [issue](https://github.com/SEU_USUARIO/RoboWordpress/issues)
- Entre em contato via email

## 📈 Roadmap

- [ ] Interface web para gerenciamento
- [ ] Suporte a múltiplos sites WordPress
- [ ] Agendamento de publicações
- [ ] Análise de performance SEO
- [ ] Integração com mais APIs de IA

## 🌐 Deploy para Acesso Remoto

### Para Estagiários e Equipe

O projeto inclui uma interface web moderna que pode ser acessada remotamente:

**Opções de Deploy:**

1. **🥇 Streamlit Cloud (Gratuito)**
   - Deploy automático do GitHub
   - URL pública: `https://seu-app.streamlit.app`
   - Configuração em 5 minutos

2. **🥈 Rede Local**
   - Rodar em seu computador
   - Estagiário acessa via IP local
   - Ideal para uso interno

3. **🥉 VPS/Servidor**
   - Controle total
   - Domínio personalizado

**Ver guia completo:** [DEPLOY.md](DEPLOY.md)

---

⭐ Se este projeto te ajudou, considere dar uma estrela!
