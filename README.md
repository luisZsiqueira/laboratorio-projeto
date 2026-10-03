# laboratorio-projeto: micro-API de gestão de tarefas

> **Status:** em desenvolvimento. Este README descreve o projeto planejado; as seções são atualizadas a cada *release*.

Micro-API REST de gestão de tarefas (*To-Do List*) com prioridades, em Python, FastAPI e SQLite3. É o miniprojeto acadêmico do curso 1 da pós-graduação SWE-GENAI, que exige o uso de IA generativa em todo o ciclo de vida do software.

## Objetivo

Entregar um MVP pequeno, claro, funcional, bem testado e bem documentado, que um avaliador consiga clonar, instalar, executar e testar em uma máquina limpa.

### Escopo do MVP

- Criar, listar (com filtro por *status*), consultar, atualizar (total e parcial), marcar como concluída e excluir tarefas.
- Cada tarefa tem uma prioridade e pode ser **aberta** (sem data/hora) ou **específica** (com data/hora estipulada).
- *Health check* real da aplicação e do banco de dados (`/health`).
- Assessor de prioridade (`priority_advisor`) com regras determinísticas, sem IA. Por exemplo: verificar se a prioridade é coerente com a data/hora e sugerir uma prioridade pela proximidade do prazo.

### Prioridades

| Valor | Significado |
| --- | --- |
| 1 | Mandatória: fazer imediatamente |
| 2 | Importante: fazer hoje, se possível |
| 3 | Regular: fazer quando houver tempo |
| 4 | Agendada: fazer na data/hora estipulada |

## Stack

| Componente | Uso |
| --- | --- |
| Python 3.11+ | linguagem |
| FastAPI | framework web e documentação OpenAPI |
| Uvicorn | servidor ASGI |
| SQLAlchemy 2.x | ORM (`Mapped` / `mapped_column`) |
| Pydantic v2 e pydantic-settings | validação de dados e configuração por variáveis de ambiente |
| SQLite3 | banco de dados |
| pytest e `TestClient` | testes unitários e de integração |
| mypy | checagem estática de tipos |
| Mermaid.js | diagramas de arquitetura (renderizados pelo GitHub) |

As versões serão fixadas no `requirements.txt`, depois de verificadas no PyPI.

Arquitetura em camadas: Controller (`app/api/`) → Service (`app/services/`) → Repository (`app/repositories/`) → SQLite3. Os detalhes e as decisões de projeto estarão em [`docs/arquitetura.md`](docs/arquitetura.md).

## Como rodar localmente

> Os comandos abaixo valem a partir da criação do `requirements.txt` e do código da aplicação, previstos na *release* `v0.1.0`.

Pré-requisitos: Python 3.11 ou superior e Git.

### 1. Clonar o repositório

```bash
git clone https://github.com/luisZsiqueira/laboratorio-projeto.git
cd laboratorio-projeto
```

### 2. Criar e ativar o ambiente virtual

PowerShell (Windows):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Bash (Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 4. Rodar a API em desenvolvimento

```bash
python -m uvicorn app.main:app --reload
```

A API fica disponível em `http://127.0.0.1:8000`, e a documentação interativa em `http://127.0.0.1:8000/docs`.

### 5. Rodar os testes e a checagem de tipos

```bash
python -m pytest -W error
python -m mypy app
```

Todos os comandos são executados a partir da raiz do repositório, com o `.venv` ativo.

## Roadmap de releases

| Release | Conteúdo | Situação |
| --- | --- | --- |
| `v0.1.0` | MVP: estrutura e documentação base, dependências verificadas, arquitetura e ADRs, configuração por ambiente, CRUD de tarefas com filtro por *status*, prioridades, `priority_advisor`, `/health` e testes | em andamento |
| `v1.0.0` | Entrega do curso: revisão de segurança e de documentação, validação em máquina limpa, histórico de uso de IA consolidado; marcada com *tag* e *release* `v1.0.0` no GitHub | planejada |

## Uso de IA generativa

O projeto é desenvolvido com apoio de IA generativa em todas as etapas do ciclo de vida: planejamento, arquitetura, código, testes e documentação.

| Assistente | Modelo | Etapas |
| --- | --- | --- |
| Claude Code | Claude Opus 5.5 | estrutura do projeto, `.gitignore`, README |

- As regras de trabalho com o assistente estão em [`CLAUDE.md`](CLAUDE.md).
- Cada *prompt* usado fica registrado em [`prompts/`](prompts/), um arquivo por *prompt*.
- O histórico de uso da IA (etapas, ganhos, desafios) estará em [`docs/HISTORY-IA.md`](docs/HISTORY-IA.md).

Todo código gerado por IA é revisado e testado antes de ser incorporado.

## Limitações e próximos passos

Fora do escopo do MVP. São possibilidades futuras, não compromissos:

- autenticação e usuários;
- paginação na listagem;
- *frontend*;
- migrações de banco com Alembic;
- priorização assistida por IA (agente via API Claude).

## Créditos e licença

Desenvolvido por Luis Z Siqueira, com apoio do Claude Code, como miniprojeto do curso 1 da pós-graduação SWE-GENAI.

Distribuído sob a licença MIT.
