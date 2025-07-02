# RoboWordpress 🤖

Um robô automatizado para criação de conteúdo SEO no WordPress usando OpenAI e Google Sheets.

## 📋 Descrição

Este projeto é um sistema automatizado que:
- Lê tópicos de uma planilha do Google Sheets
- Gera conteúdo otimizado para SEO usando OpenAI
- Publica automaticamente no WordPress
- Inclui testes de conexão e funcionalidade

## 🚀 Funcionalidades

- ✅ Integração com Google Sheets para gerenciar tópicos
- ✅ Geração automática de conteúdo usando OpenAI GPT
- ✅ Publicação automática no WordPress
- ✅ Testes de conectividade
- ✅ Scripts de execução automatizada

## 📁 Estrutura do Projeto

```
RoboWordpress/
├── robo_pillot_v2.py      # Versão principal do robô
├── robo_pilloto.py        # Versão alternativa
├── robo_simples.py        # Versão simplificada
├── teste_conexao_wordpress.py  # Teste de conexão WordPress
├── teste_sheets.py        # Teste de conexão Google Sheets
├── teste_wordpress.py     # Testes WordPress
├── teste.py               # Testes gerais
├── executar_teste.sh      # Script de execução
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

### Execução Principal
```bash
python robo_pillot_v2.py
```

### Testes
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

---

⭐ Se este projeto te ajudou, considere dar uma estrela!
