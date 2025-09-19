
# Sumário

- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Execução](#instalação-e-execução)
- [Arquitetura do Projeto](#arquitetura-do-projeto)
- [Descrição dos Módulos](#descrição-dos-módulos)

---

## Estrutura do Projeto

- `main.py`: Ponto de entrada do projeto.
- `packages/`: Contém os pacotes `domain`, `application` e `infrastructure`.
- `requirements.txt`: Lista os pacotes locais para instalação via pip.
- `pyproject.toml`: Configuração do workspace e dependências.

---

## Instalação e Execução

### 1. Usando ambiente virtual (`venv`) e pip

**Pré-requisitos:**  
- Python 3.13+

**Crie o ambiente virtual:**

```pwsh
python -m venv .venv
```

**Ative o ambiente virtual:**

- **Windows:**
  ```pwsh
  .venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```pwsh
  source .venv/bin/activate
  ```

**Instale as dependências:**

```pwsh
pip install -r requirements.txt
```


**Execução:**

*Exemplo:*
`python main.py <termo_de_busca>`
```pwsh
python main.py casa
```

> **Observação:** Não é necessário rodar manualmente o módulo `create_database.py`. O banco de dados será criado automaticamente quando o projeto for executado.

---

### 2. Usando [uv](https://github.com/astral-sh/uv)

O `uv` é um gerenciador de dependências rápido para Python.

**Pré-requisitos:**
- [uv instalado](https://github.com/astral-sh/uv#installation)

**Instalação das dependências:**

```pwsh
uv sync --no-group dev
```

**Execução:**

*Exemplo:*
`uv run main.py <termo_de_busca>`
```pwsh
uv run main.py casa
```

---

## Arquitetura do Projeto

```
leading-scraping/
│
├── main.py                               # Ponto de entrada do projeto
├── requirements.txt                      # Dependências do projeto
├── pyproject.toml                        # Configuração do workspace
└── packages/
  ├── domain/                             # Camada de regras de negócio
  │   └── src/domain/
  │       ├── models/
  │       │   └── products.py             # Entidade Produto
  │       ├── interfaces/
  │       │   ├── scrapers.py             # Interface para scrapers
  │       │   └── repositories.py         # Interface para repositórios
  │       └── validations/
  │           └── exceptions.py           # Exceções do domínio
  ├── application/                        # Camada de orquestração e serviços
  │   └── src/application/
  │       ├── interfaces/
  │       │   └── process.py              # Interface de processo de scraping
  │       └── services/
  │           └── process_scrapping.py    # Serviço de execução do scraping
  └── infrastructure/                     # Camada de integração externa e persistência
    └── src/infrastructure/
      ├── scrapper/
      │   ├── http_client.py              # Cliente HTTP para requisições
      │   └── maeto_scrapper.py           # Scraper específico do site Loja Maeto
      ├── repositories/
      │   └── sqlite_local.py             # Persistência local com SQLite
      └── validations/
          └── exceptions.py               # Exceções da infraestrutura
```

---

### Descrição dos Módulos

#### domain
- **models/products.py**: Define a entidade Produto e seus atributos.
- **interfaces/scrapers.py**: Define as interfaces para scrapers, abstraindo a lógica de coleta de dados.
- **interfaces/repositories.py**: Interfaces para repositórios, abstraindo persistência de dados.
- **validations/exceptions.py**: Exceções e validações específicas do domínio.

#### application
- **interfaces/process.py**: Interface para processos de aplicação, como orquestração de scraping.
- **services/process_scrapping.py**: Serviço responsável por executar o processo de scraping, integrando domínio e infraestrutura.

#### infrastructure
- **scrapper/http_client.py**: Implementa o cliente HTTP para requisições externas.
- **scrapper/maeto_scrapper.py**: Scraper específico para o site Loja Maeto.
- **repositories/sqlite_local.py**: Implementa persistência local usando SQLite.
- **validations/exceptions.py**: Exceções e validações específicas da infraestrutura.

Cada módulo segue o padrão de separação de responsabilidades, facilitando manutenção, testes e evolução do projeto.

---
