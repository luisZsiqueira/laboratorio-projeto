# laboratorio-projeto: micro-API de gestão de tarefas

> **Status:** em desenvolvimento. A *release* `v0.1.0` (fundação: documentação, dependências e arquitetura) está publicada; o código da aplicação começa na `v0.2.0`. As mudanças de cada *release* estão no [`CHANGELOG.md`](CHANGELOG.md).

Micro-API REST de gestão de tarefas (*To-Do List*) com prioridades, em Python, FastAPI e SQLite3. É o miniprojeto acadêmico do curso 1 da pós-graduação SWE-GENAI, que exige o uso de IA generativa em todo o ciclo de vida do software.

## Objetivo

Entregar um MVP pequeno, claro, funcional, bem testado e bem documentado, que um avaliador consiga clonar, instalar, executar e testar em uma máquina limpa.

### Escopo do MVP

- Criar, listar (com filtro por *status*), consultar, atualizar (total e parcial), marcar como concluída e excluir tarefas.
- Cada tarefa tem uma prioridade e pode ser **aberta** (sem data/hora) ou **específica** (com data/hora estipulada).
- *Health check* real da aplicação e do banco de dados (`/health`).
- Assessor de prioridade (`priority_advisor`) com regras determinísticas, sem IA. Por exemplo: verificar se a prioridade é coerente com a data/hora e sugerir uma prioridade pela proximidade do prazo.

Os requisitos funcionais e não funcionais, com critérios de aceitação, os itens fora de escopo e as decisões em aberto estão em [`docs/escopo-mvp.md`](docs/escopo-mvp.md).

### Prioridades

| Valor | Significado |
| --- | --- |
| 1 | Mandatória: fazer imediatamente |
| 2 | Importante: fazer hoje, se possível |
| 3 | Regular: fazer quando houver tempo |
| 4 | Agendada: fazer na data/hora estipulada |

## Stack

| Componente | Versão | Uso |
| --- | --- | --- |
| Python | 3.11+ (testado em 3.14.6) | linguagem |
| FastAPI | 0.142.2 | framework web e documentação OpenAPI |
| Starlette | 1.7.0 | base do FastAPI (dependência transitiva) |
| Uvicorn | 0.54.0 | servidor ASGI |
| SQLAlchemy | 2.1.3 | ORM (`Mapped` / `mapped_column`) |
| Pydantic | 2.13.5 | validação de dados |
| pydantic-settings | 2.15.0 | configuração por variáveis de ambiente |
| SQLite3 | embutido no Python | banco de dados |
| pytest | 9.1.1 | testes unitários e de integração |
| httpx2 | 2.13.1 | cliente HTTP do `TestClient` |
| mypy | 2.4.0 | checagem estática de tipos |
| Mermaid.js | renderizado pelo GitHub | diagramas de arquitetura |

As versões estão fixadas no [`requirements.txt`](requirements.txt), incluindo as dependências transitivas. Elas foram consultadas no PyPI em 03/10/2026. O Python 3.11 é o mínimo porque o SQLAlchemy 2.1 o exige.

## Arquitetura

API síncrona em camadas, uma por pacote em `app/`:

```mermaid
flowchart LR
    C(["Cliente HTTP"]) --> API["app/api<br/>rotas"]
    API --> SVC["app/services<br/>regras de negócio"]
    SVC --> REPO["app/repositories<br/>acesso ao banco"]
    REPO --> DB[("SQLite3")]
    MOD["app/models<br/>ORM, esquemas, settings"] -.-> API
    MOD -.-> SVC
    MOD -.-> REPO
```

Os módulos e suas dependências, o fluxo de dados de `POST /tasks`, `GET /health` e dos erros em `/tasks/{id}`, o modelo de dados, a estratégia de testes e as decisões de arquitetura (ADRs) estão em [`docs/arquitetura.md`](docs/arquitetura.md). O histórico visual dos diagramas, com o antes e o depois de cada revisão, está em [`docs/mermaid.md`](docs/mermaid.md).

## Configuração

Toda configuração vem de variáveis de ambiente, opcionalmente lidas de um arquivo `.env` na raiz do repositório. O `.env` não é versionado.

| Variável | Valores | Padrão | Descrição |
| --- | --- | --- | --- |
| `DATABASE_URL` | URL do SQLAlchemy | `sqlite:///./tasks.db` | banco de dados; cria o arquivo `tasks.db` na raiz |
| `ENVIRONMENT` | `development`, `test`, `production` | `development` | em `production`, a documentação interativa (`/docs`, `/redoc`) fica desabilitada |

Exemplo de `.env`:

```dotenv
DATABASE_URL=sqlite:///./tasks.db
ENVIRONMENT=development
```

## Como rodar localmente

> A instalação das dependências já funciona. Os comandos de execução da API e dos testes passam a valer quando o código da aplicação existir, a partir da *release* `v0.2.0`.

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
python -m mypy --explicit-package-bases app
```

Todos os comandos são executados a partir da raiz do repositório, com o `.venv` ativo. O `--explicit-package-bases` é necessário porque `app/` não tem `__init__.py` na raiz (ADR-03 e ADR-11 em [`docs/arquitetura.md`](docs/arquitetura.md)).

### Solução de problemas (Windows)

Se `import sqlalchemy` falhar com `DLL load failed while importing _immutabledict_cy` e a mensagem "Uma política de Controle de Aplicativo bloqueou este arquivo", o Smart App Control do Windows está bloqueando as extensões compiladas do SQLAlchemy, que não são assinadas. Reinstale a mesma versão em Python puro, com o `.venv` ativo:

```powershell
$env:DISABLE_SQLALCHEMY_CEXT="1"
python -m pip install --force-reinstall --no-deps --no-binary SQLAlchemy SQLAlchemy==2.1.3
Remove-Item Env:DISABLE_SQLALCHEMY_CEXT
```

A versão e o comportamento são os mesmos; só as otimizações em Cython ficam de fora.

## Roadmap de releases

Os itens de cada *release* (requisitos funcionais RF e técnicos RT), com critérios de aceite e estimativas, estão em [`docs/backlog.md`](docs/backlog.md).

| Release | Conteúdo | Situação |
| --- | --- | --- |
| `v0.1.0` | Fundação: estrutura, `.gitignore`, README, requisitos do curso, dependências verificadas, arquitetura e ADRs | concluída (04/10/2026, *tag* `v0.1.0`) |
| `v0.2.0` | Base técnica: configuração por ambiente, banco SQLite, aplicação FastAPI com `lifespan` e `/health` | planejada |
| `v0.3.0` | CRUD de tarefas: criar, listar com filtro por *status*, consultar, atualizar (total e parcial), concluir e excluir | planejada |
| `v0.4.0` | Prioridades e `priority_advisor` (regras determinísticas) | planejada |
| `v0.5.0` | Revisão da arquitetura, de segurança e da documentação | planejada |
| `v1.0.0` | Entrega do curso: validação em máquina limpa, histórico de uso de IA consolidado; marcada com *tag* e *release* `v1.0.0` no GitHub | planejada |

## Uso de IA generativa

O projeto é desenvolvido com apoio de IA generativa em todas as etapas do ciclo de vida: planejamento, arquitetura, código, testes e documentação.

| Assistente | Modelo | Etapas |
| --- | --- | --- |
| Claude (*chat*) | Claude Opus 5.5 | concepção do `CLAUDE.md` inicial a partir dos requisitos do curso, em 01 e 02/10/2026, antes do repositório |
| Claude Code | Claude Opus 5.5 | estrutura do projeto, `.gitignore`, README, verificação de versões e `requirements.txt`, desenho da arquitetura, licença, histórico de uso de IA, revisão de segredos e publicação no GitHub, revisão de publicação da `v0.1.0` (APIs deprecadas, ambiente virtual, *commits*, `CHANGELOG.md`), documento de escopo e requisitos do MVP, backlog por *release*, revisão dos diagramas Mermaid, regras de código e de *blueprint* executável |
| Claude in Chrome | Claude Opus 5.5 | conferência visual da renderização dos diagramas Mermaid no GitHub (Prompts 07 e 12) |
| Claude (*chat*) | Claude Sonnet 5.5 | extração, a partir de capturas de tela do curso, dos *prompts* de exemplo do tutor ([`docs/release-prompts-solon-020.md`](docs/release-prompts-solon-020.md)), em 04/10/2026 |
| Claude Code | Claude Fable 5.1 | planejamento dos *prompts* da fase de desenvolvimento ([`prompts/prompts-desenvolvimento.md`](prompts/prompts-desenvolvimento.md), Prompt 20) |

- As regras de trabalho com o assistente estão em [`CLAUDE.md`](CLAUDE.md).
- Cada *prompt* usado fica registrado em [`prompts/`](prompts/), um arquivo por *prompt*; os *prompts* planejados para as *releases* `v0.2.0` a `v1.0.0` estão em [`prompts/prompts-desenvolvimento.md`](prompts/prompts-desenvolvimento.md).
- O histórico de uso da IA (etapas, ganhos, desafios) está em [`docs/HISTORY-IA.md`](docs/HISTORY-IA.md); o uso anterior ao repositório, em [`docs/PRE-HISTORY-IA.md`](docs/PRE-HISTORY-IA.md); o uso em modo *chat* fora do repositório, em [`docs/EXTRA-HISTORY-IA.md`](docs/EXTRA-HISTORY-IA.md).
- Os *blueprints* aprovados são escritos para que um modelo de execução, como o Claude Sonnet 5.5, os siga sem depender do contexto da conversa (regra em [`CLAUDE.md`](CLAUDE.md), Blueprint executável).

Todo código gerado por IA é revisado e testado antes de ser incorporado.

## Limitações e próximos passos

Fora do escopo do MVP. São possibilidades futuras, não compromissos:

- autenticação e usuários;
- paginação na listagem;
- *frontend*;
- migrações de banco com Alembic;
- priorização assistida por IA (agente via API Claude).

O motivo de cada item ficar fora do MVP e os itens excluídos sem previsão estão em [`docs/escopo-mvp.md`](docs/escopo-mvp.md) (Fora de escopo).

## Créditos e licença

Desenvolvido por Luis Z Siqueira, com apoio do Claude Code, como miniprojeto do curso 1 da pós-graduação SWE-GENAI.

Distribuído sob a licença MIT. Veja o arquivo [`LICENSE`](LICENSE).
