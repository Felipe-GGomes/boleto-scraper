# 1. 🤖 Boleto Scraper — Automação com Python & Selenium

> Automatiza a coleta de boletos mensais de duas fontes diferentes e salva os PDFs localmente.

---

## 💡 Motivação

Cansado de entrar todo mês em dois sistemas diferentes para buscar boletos, criei essa automação para fazer isso com um único comando.

- 🎓 **Portal acadêmico** (sistema Jacad) — via Selenium
- 📧 **E-mail do condomínio** (Gmail) — via IMAP

---

## 🚀 Funcionalidades

- ✅ Login automático no portal acadêmico
- ✅ Detecção inteligente de boletos com pagamento habilitado
- ✅ Download de **todos** os boletos em aberto de uma vez
- ✅ Conexão IMAP com Gmail para buscar e-mails da administradora
- ✅ Extração do link e download do boleto do condomínio em PDF
- ✅ Credenciais protegidas via `.env` — nada no código

---

## 🗂️ Estrutura do Projeto

boleto-scraper/

├── main.py # Ponto de entrada

├── uniguairaca.py # Módulo do portal acadêmico (Selenium)

├── condominio.py # Módulo do e-mail (IMAP)

├── .env.example # Exemplo de configuração — copie e renomeie para .env

└── requirements.txt


---

## ⚙️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| Selenium | Automação e navegação no portal acadêmico |
| WebDriver Manager | Gerencia o ChromeDriver automaticamente |
| imaplib | Conexão com Gmail via IMAP |
| python-dotenv | Variáveis de ambiente |

---

## 🔧 Como configurar

### 1. Clone o repositório

git clone https://github.com/seu-usuario/boleto-scraper.git
cd boleto-scraper

# 2. Crie o ambiente virtual
python -m venv .venv

## Windows
.venv\Scripts\activate

## Linux/Mac
source .venv/bin/activate

# 3. Instale as dependências 
pip install -r requirements.txt

4. Configure as variáveis de ambiente
## Copie o arquivo de exemplo
cp .env.example .env

## Edite o .env com seus dados

# 5. Crie a pasta de saída dos PDFs
## Windows
mkdir Boletos

## Linux/Mac
mkdir boletos

# 6. Execute
python main.py

# 7. 📋 Como funciona

python main.py
│

├──► uniguairaca.py

│       ├── Abre o Chrome com Selenium

│       ├── Faz login no portal acadêmico

│       ├── Abre nova aba em /financeiro

│       ├── Varre a tabela de parcelas

│       ├── Identifica boletos com botão ativo

│       └── Baixa todos os PDFs encontrados

│

└──► condominio.py

        ├── Conecta ao Gmail via IMAP

        ├── Busca e-mails da administradora

        ├── Extrai o link do boleto mais recente

        └── Faz o download do PDF

# 8. 📄 Licença
MIT — sinta-se livre para adaptar ao seu caso de uso.
