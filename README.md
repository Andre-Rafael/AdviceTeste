# AdviceTeste

Repositório: [github.com/Andre-Rafael/AdviceTeste](https://github.com/Andre-Rafael/AdviceTeste.git)

Aplicação para captura automatizada de dados de processos judiciais no site do Tribunal de Justiça do Estado de Minas Gerais (TJMG), a partir de uma lista de nomes de partes.

## 📋 Pré-requisitos

- [Python 3.13](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation) (gerenciador de dependências)
- Uma chave de API do [2Captcha](https://2captcha.com/), necessária para a resolução automática do reCAPTCHA presente na página do TJMG

## 🔧 Instalação

Clone o repositório:

```bash
git clone https://github.com/Andre-Rafael/AdviceTeste.git
cd AdviceTeste
```

Instale as dependências com o Poetry:

```bash
poetry install
```

## ⚙️ Configuração

A aplicação depende de um token de API do 2Captcha para resolver o reCAPTCHA da página consultada. Configure-o de uma das seguintes formas:

**Opção 1: arquivo `.env`**

Crie um arquivo `.env` na raiz do projeto com o conteúdo:

```env
TWOCAPTCHA_API_KEY=sua_chave_aqui
```

**Opção 2: variável de ambiente**

```bash
export TWOCAPTCHA_API_KEY=sua_chave_aqui
```

> ⚠️ Sem esse token configurado, a aplicação não conseguirá contornar o reCAPTCHA e a coleta de dados falhará.

## ▶️ Como executar

```bash
poetry run python advice_crawler/main.py
```

A aplicação percorrerá a lista de nomes definida no código-fonte e consultará cada um deles no site do TJMG. A lista padrão inclui:

- ADILSON DA SILVA
- JOÂO DA SILVA MORAES
- RICARDO DE JESUS
- SERGIO FIRMINO DA SILVA
- HELENA FARIAS DE LIMA
- PAULO SALIM MALUF
- PEDRO DE SA

## 📂 Saída gerada

Ao final da execução, dois arquivos são criados na raiz do projeto:

| Arquivo | Descrição |
|---|---|
| `data_collected.json` | Dados coletados em formato JSON |
| `tjmg.db` | Banco de dados SQLite com os dados coletados |

## 📝 Observações

- O tempo de execução depende diretamente do tempo de resposta do serviço de resolução de CAPTCHA e da quantidade de nomes consultados.
- Use os dados coletados de acordo com as diretrizes de uso de dados públicos do TJMG.