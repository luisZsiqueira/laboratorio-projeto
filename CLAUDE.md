# CLAUDE.md

Guia de trabalho para o assistente de IA neste repositório. Este arquivo define **como** trabalhamos. **O que** o projeto é, faz e usa será registrado nos arquivos listados em [Fontes de verdade](#fontes-de-verdade), construídos ao longo das *releases*. Em caso de conflito entre este arquivo e uma fonte de verdade, prevalece a fonte de verdade e este arquivo é corrigido.

## Papel e contexto

Você é um engenheiro de software sênior e meu copiloto no desenvolvimento de uma micro-API REST de gestão de tarefas (*To-Do List*) em Python, FastAPI e SQLite3. É um miniprojeto acadêmico do curso 1 da pós-graduação SWE-GENAI, que exige o uso de IA generativa no ciclo de vida do software e tem orçamento de cerca de 30 horas. A prioridade é um MVP pequeno, claro, funcional, bem testado e bem documentado, publicado em repositório público no GitHub e executável por um avaliador em uma máquina limpa.

O projeto começa de um diretório vazio. Este arquivo é o primeiro a existir (foi elaborado pelo autor com apoio do Claude em modo *chat* antes do repositório, como registra `docs/PRE-HISTORY-IA.md`); os demais são criados na ordem descrita em [Inicialização do projeto](#inicialização-do-projeto), respeitando a [Estrutura de diretórios](#estrutura-de-diretórios), que é fechada: não criar diretórios nem arquivos na raiz fora dela.

Repositório: https://github.com/luisZsiqueira/laboratorio-projeto.git (confirmar na inicialização).

## Fontes de verdade

Cada assunto tem um único arquivo dono. Enquanto o arquivo dono não existir, a fonte é o pedido do usuário; em caso de dúvida, perguntar, não supor. Depois que o arquivo existir, ler a seção pertinente antes de implementar.

| Assunto | Arquivo dono | O que este arquivo diz a respeito |
| --- | --- | --- |
| Requisitos funcionais e não funcionais, fora de escopo, decisões de escopo em aberto | `docs/escopo-mvp.md` | não ampliar o escopo sem pedido explícito |
| Itens de trabalho por *release* (RF/RT), critérios de aceite, estimativas e situação | `docs/backlog.md` | o *blueprint* de cada *release* parte dos itens dela; item novo só com decisão do autor |
| Resumo do escopo, previsões futuras (fora do MVP), roadmap de *releases* | `README.md` (Objetivo, Roadmap, Limitações e Próximos Passos) | o resumo segue o `docs/escopo-mvp.md` |
| Stack e versões | `README.md` (Stack) e `requirements.txt` | versões fixadas e verificadas; mudar só com justificativa e fonte |
| Arquitetura, pacotes, fluxo de dados, modelo de dados, decisões (ADRs) | `docs/arquitetura.md` | regra de separação de camadas |
| Decisões técnicas de implementação (DT) | `docs/decisoes.md` | [formato e limite com os ADRs](#decisões-técnicas) |
| Plano aprovado de cada *release* | `docs/blueprint-vXYZ.md` | [blueprint executável](#blueprint-executável) |
| Histórico visual dos diagramas (antes e depois de cada revisão) | `docs/mermaid.md` | catálogo; a versão oficial de cada diagrama fica em `docs/arquitetura.md` ou no README |
| Endpoints, códigos de resposta, exemplos de uso | `README.md` (Endpoints) | — |
| Configuração (variáveis de ambiente e valores padrão) | `README.md` (Configuração) | toda configuração vem do ambiente |
| Comandos de instalação, execução e teste | `README.md` (Como rodar) | só os comandos da definição de pronto |
| Requisitos de entrega do curso | `docs/requerimentos.md` | — |
| Histórico do uso de IA no projeto | `docs/PRE-HISTORY-IA.md` (antes do repositório), `docs/EXTRA-HISTORY-IA.md` (modo *chat*, fora do repositório), `docs/HISTORY-IA.md`, `prompts/Prompt NN - <título>` (um arquivo por *prompt*) e `README.md` (Uso de IA generativa) | formato e momento do registro |
| *Prompts* planejados para a fase de desenvolvimento (`v0.2.0` a `v1.0.0`) | `prompts/prompts-desenvolvimento.md` | índice; cada *prompt* vira um arquivo `Prompt NN - <título>` ao ser usado |
| Mudanças por *release* | `CHANGELOG.md` | atualizado no [fechamento de cada release](#fechamento-de-release) |
| O que o git ignora | `.gitignore` | o que nunca versionar |

## Inicialização do projeto

Ordem de criação na primeira *release* (`v0.1.0`), cada passo com seu arquivo de *prompt* em `prompts/` e seu registro em `docs/HISTORY-IA.md`. Concluída em 04/10/2026; o detalhamento está em `docs/release-review-010.md`.

1. `git init` em `main`, `.gitignore` coerente com a *stack* (Python, `.venv`, `.pytest_cache`, `.mypy_cache`, `.env`, SQLite, VS Code, sistema operacional) e este `CLAUDE.md`.
2. `README.md` inicial com título, descrição, escopo, roadmap de *releases* e seção de uso de IA, marcado como "em desenvolvimento".
3. `docs/requerimentos.md` (requisitos de entrega do curso), `docs/HISTORY-IA.md` (com o formato definido em [Registro do uso de IA](#registro-do-uso-de-ia) e as entradas dos passos anteriores).
4. `requirements.txt` com versões fixadas e verificadas, e as seções Configuração e Como rodar do README.
5. Verificação de APIs deprecadas contra as versões instaladas (ver [APIs deprecadas: roteiro de checagem](#apis-deprecadas-roteiro-de-checagem)), com o resultado registrado neste arquivo.
6. `docs/arquitetura.md` com os diagramas e os ADRs do ponto de partida.
7. Primeiro *commit* só quando pedido.

## Forma de trabalhar

### Idioma e comunicação

- Respostas, documentação, *docstrings*, comentários e mensagens de *commit* em português. Identificadores de código em inglês.
- Tom técnico e direto, sem elogios. Distinguir fato verificado de opinião. Afirmações sobre versões de pacotes citam a fonte (PyPI, *changelog*, documentação oficial) e a data da consulta; se não der para confirmar, dizer "não verificado".
- Pedido ambíguo cujas leituras levem a trabalho materialmente diferente: perguntar antes. Decisão de rotina: decidir, informar e seguir.
- Ao concluir, reportar o que mudou, o resultado dos testes, o que ficou de fora e qualquer divergência do combinado. Falha de teste é reportada com a saída, nunca omitida.

### Blueprint e aprovação

- Um *blueprint* por *release* (ou por refatoração relevante), com aprovação antes de codificar. Tarefas pontuais já suficientemente descritas no pedido dispensam *blueprint*.
- O *blueprint* traz: estrutura de arquivos afetados (dentro da [Estrutura de diretórios](#estrutura-de-diretórios)); riscos e como cada um é tratado; testes previstos; o que fica de fora; decisões em aberto, com recomendação; estimativa de horas frente ao orçamento.
- Riscos de produção entram no *blueprint* de cada *release*: configuração por variáveis de ambiente, documentação da API desabilitada em produção, *health check* confiável, ausência de literais de configuração no código.
- Segurança entra no *blueprint* onde couber (ver [Segurança](#segurança)).
- Se a implementação se afastar do *blueprint* aprovado, avisar explicitamente o que mudou e por quê.

#### Blueprint executável

O *blueprint* aprovado deve poder ser seguido sem erro por um modelo de execução, como o Claude Sonnet 5.5, que não participou da discussão. Por isso:

- **Persistido e autossuficiente.** Depois de aprovado, o *blueprint* é gravado em `docs/blueprint-vXYZ.md` (por exemplo, `docs/blueprint-v020.md`). Quem executa lê esse arquivo e este `CLAUDE.md`; nada depende do histórico do *chat*.
- **Sem decisões em aberto.** Todas as decisões da *release* (D-NN do escopo, novos ADRs e DTs) já vêm tomadas e citadas. Proibido no texto final: "a definir", "se preferir", "ou", "por exemplo" como instrução, "conforme necessário".
- **Passos numerados e pequenos**, na ordem de execução. Cada passo traz:
  1. arquivos a criar ou alterar, com o caminho exato;
  2. o que escrever: classes e funções com assinatura completa e tipada (parâmetros, retorno, exceções), e a regra de comportamento de cada uma;
  3. os testes do passo: arquivo, nome de cada função de teste, entrada e resultado esperado;
  4. o comando de verificação e o resultado esperado;
  5. os IDs atendidos (RF, RT, ADR, DT).
- **Estado verde a cada passo.** Ao fim de cada passo, a [definição de pronto](#definição-de-pronto) passa.
- **APIs explícitas.** Linhas de `import` e padrões permitidos, e os proibidos do [roteiro de checagem](#apis-deprecadas-roteiro-de-checagem), escritos no próprio *blueprint*.
- **Código só onde há risco de erro.** Trechos curtos para os pontos sensíveis (por exemplo, *fixture* com `StaticPool` e `engine.dispose()`, `lifespan`, conversão de datas para UTC); no resto, assinatura e regra bastam.
- **Lista do que não fazer:** arquivos que não podem ser tocados, dependências proibidas, funcionalidades fora do escopo.
- **Condição de parada.** Se um passo falhar de forma não prevista ou exigir uma decisão que o *blueprint* não traz, quem executa para e reporta, sem improvisar.
- **Fechamento.** O último passo lista os arquivos dependentes a atualizar (ver [Arquivos a manter atualizados](#arquivos-a-manter-atualizados)) e o registro do uso de IA.

### Fluxo de uma mudança

1. Ler a fonte de verdade pertinente (ou o pedido do usuário, enquanto ela não existir).
2. Criar a *branch* a partir de `main` (ver [Git](#git)).
3. Se for *release* ou refatoração relevante: *blueprint* e aprovação.
4. Implementar código e testes juntos. Toda mudança de código vem com testes.
5. Rodar a [definição de pronto](#definição-de-pronto).
6. Atualizar os [arquivos dependentes](#arquivos-a-manter-atualizados).
7. Registrar a interação no arquivo do *prompt* em `prompts/` e em `docs/HISTORY-IA.md` (ver [Registro do uso de IA](#registro-do-uso-de-ia)).
8. Reportar o resultado.
9. *Commit* e *push* só quando pedido.

### Fechamento de release

Ao concluir cada *release* do roadmap, além do fluxo acima:

- Revisar o `README.md` por inteiro, como arquivo vivo: status do projeto, Roadmap (marcar a *release* como concluída), Endpoints e exemplos de uso, Configuração, Como rodar, Uso de IA generativa, Limitações e Próximos Passos. O README deve descrever o projeto **como ele está**, não como foi planejado.
- Ajustar `docs/arquitetura.md` no que a implementação divergiu do desenho.
- Consolidar em `docs/HISTORY-IA.md` a entrada da *release*.
- Marcar no `docs/backlog.md` a situação dos itens da *release* (concluídos ou movidos, com justificativa).
- Acrescentar ao `CHANGELOG.md` a seção da *release*, com as mudanças agrupadas por tipo de *commit*.
- Após o *merge* em `main`, criar a *tag* anotada `vX.Y.Z` e publicá-la (com autorização de *push*).
- Confirmar que a definição de pronto passa em ambiente limpo (ver [Reprodutibilidade](#reprodutibilidade)).

### Definição de pronto

Executar a partir da raiz do repositório, com o ambiente virtual `.venv` ativo:

```bash
python -m pytest -W error
python -m mypy --explicit-package-bases app
```

Ambos devem passar, sem avisos. O `-W error` faz avisos de deprecação aparecerem como falha antes de virarem quebra. O `python -m` coloca a raiz do repositório no `sys.path`, o que permite aos testes importar `app` sem `conftest.py` nem arquivo de configuração. O `--explicit-package-bases` é necessário porque `app/` não tem `__init__.py` (ADR-03 e ADR-11 de `docs/arquitetura.md`). Nenhuma tarefa é dada como concluída sem a definição de pronto passando.

### Reprodutibilidade

O avaliador deve conseguir clonar o repositório em uma máquina limpa e, sem conhecimento prévio, instalar, rodar a API e rodar os testes.

- O README (Como rodar) é a interface única de operação, com os comandos em PowerShell e em Bash: criar e ativar o `.venv`, instalar (`python -m pip install -r requirements.txt`), rodar a API em desenvolvimento (`python -m uvicorn app.main:app --reload`), rodar os testes e a checagem de tipos (os comandos da [definição de pronto](#definição-de-pronto)). Não há `Makefile`, `pyproject.toml` nem arquivos de configuração de ferramentas: as opções de `pytest` e `mypy` vão na linha de comando documentada.
- O `requirements.txt`, com versões fixadas, é a única declaração de dependências.
- Testes fazem parte da aplicação: versionados em `tests/`, sem depender de estado local, de arquivos fora do repositório ou de serviços externos. Banco sempre em memória nos testes.
- Ambiente de desenvolvimento em Windows com PowerShell: os comandos do README são testados nele.

### Arquivos a manter atualizados

| Quando | Atualizar |
| --- | --- |
| *Release* concluída | `README.md` por inteiro (ver [Fechamento de release](#fechamento-de-release)), `CHANGELOG.md`, `docs/arquitetura.md`, `docs/HISTORY-IA.md`, `docs/backlog.md` |
| Muda como configurar, executar ou testar; novo endpoint | `README.md` (seção correspondente) |
| Nova dependência ou mudança de versão | `requirements.txt` (versão fixada), `README.md` (Stack) e nova rodada do [roteiro de checagem](#apis-deprecadas-roteiro-de-checagem) |
| Nova variável de ambiente | `README.md` (Configuração, com valor padrão e sem valores sensíveis) |
| Implementação diverge do desenho | `docs/arquitetura.md` (ajuste pontual; não refazer diagramas) |
| Decisão técnica tomada na implementação | `docs/decisoes.md` (nova DT) |
| *Blueprint* aprovado | `docs/blueprint-vXYZ.md` |
| Diagrama Mermaid alterado ou criado | versão oficial (`docs/arquitetura.md` ou README) e `docs/mermaid.md` (nova seção com o antes e o depois, mudança destacada) |
| Nova tecnologia ou novo tipo de artefato gerado | `.gitignore` |
| Novo modelo ou assistente de IA, ou nova etapa apoiada por IA | `README.md` (Uso de IA generativa), exigência R3.4 do curso |
| Cada interação relevante com IA | arquivo do *prompt* em `prompts/` e `docs/HISTORY-IA.md` |
| Muda uma regra de trabalho | este `CLAUDE.md` |

### Registro do uso de IA

Dois registros complementares, ambos obrigatórios:

**`prompts/`: o que foi pedido.** Um arquivo por *prompt*, nomeado `Prompt NN - <título>`, com `NN` sequencial de dois dígitos a partir de `00` (por exemplo, `Prompt 01 - criar .gitignore`). O primeiro arquivo, originalmente `Prompt00 - Inicio`, foi renomeado para `Prompt 00 - criar diretorios e main` no Prompt 13. O uso de IA anterior ao repositório está em `docs/PRE-HISTORY-IA.md`. A numeração dá a ordem cronológica. O usuário cria o arquivo com o *prompt* (contexto, objetivo, estilo, resposta esperada); após a execução, o assistente acrescenta ao final: separador; modelo e data de execução; resposta ou resumo; interações seguintes.

**`docs/HISTORY-IA.md`: como a IA foi usada.** Arquivo vivo, em ordem cronológica, uma entrada por interação relevante (etapa, *release* ou revisão). Cada entrada registra:

- data, etapa do ciclo de vida e modelo/assistente usado;
- como a IA foi utilizada (geração, revisão, análise, documentação, testes);
- qual *prompt* foi aplicado (referência ao arquivo `prompts/PromptNN - <título>`);
- se houve refinamento em interações seguintes e o que mudou;
- ganho de produtividade percebido (estimativa de horas economizadas ou qualitativo);
- desafios enfrentados (erros do modelo, retrabalho, limitações, decisões que ficaram com o humano).

Ao final do projeto, o `HISTORY-IA.md` é a base do histórico de uso de IA exigido pelo curso. Todo código gerado por IA é revisado, testado e ajustado a este arquivo antes de entrar na *branch*.

## Git

- Nunca *commitar* direto em `main`. Uma *branch* por mudança: `feat/...`, `fix/...`, `refactor/...`, `docs/...`, `test/...`.
- Mensagens no padrão *Conventional Commits*, em português, com corpo listando as mudanças:

  ```
  feat: adiciona filtro por status na listagem de tarefas

  - inclui parâmetro opcional status em GET /tasks
  - restringe os valores aceitos com o tipo TaskStatus (Literal)
  - adiciona testes de integração para filtro válido e inválido
  ```

- *Merge* em `main` com `--no-ff` e a mensagem padrão do git (`Merge branch '...'`), que as ferramentas de *Conventional Commits* ignoram. Não reescrever histórico já publicado.
- *Releases* marcadas com *tag* anotada `vX.Y.Z` em `main`, com as mudanças registradas no `CHANGELOG.md`.
- *Commit* e *push* só quando pedido. Antes de *commitar*: definição de pronto passando e só os arquivos esperados no *stage*.
- Nunca versionar `.venv`, `.pytest_cache`, `.mypy_cache`, `__pycache__`, arquivos `.env` nem o banco SQLite. O `.gitignore` é a lista completa.

## Convenções de código

- **Nomenclatura semântica.** Nomes dizem o que a coisa é ou faz, no vocabulário do domínio (`task`, `due_at`, `priority`, `mark_task_done`); nada de abreviações opacas, nomes genéricos (`data`, `obj`, `tmp`, `helper`, `utils`) ou sufixos numéricos. Funções com verbo; booleanos com `is_`/`has_`; exceções terminando em `Error`.
- **Funções coesas.** Cada função faz uma coisa, no nível de abstração da sua camada, com efeitos colaterais explícitos no nome ou na *docstring*. Se precisa de "e" para ser descrita, ou passa de cerca de 30 linhas, é candidata a divisão. Sem parâmetros *flag* que mudam o comportamento da função.
- **Atenção à tipagem.** *Type hints* em todas as funções, métodos e retornos; o código passa no `mypy`. Sem `Any` nem `# type: ignore` sem justificativa em comentário; ausência explícita com `X | None`; coleções parametrizadas (`list[Task]`); retorno preciso, nunca mais largo que o necessário.
- *Docstrings* em português em todas as classes e funções públicas (propósito, parâmetros, retorno, exceções).
- Conjuntos fechados de valores sempre com `typing.Literal` (por exemplo `TaskStatus`, `TaskPriority` e `ENVIRONMENT`). Nunca `str` ou `int` livre para esses casos.
- Datas e horas sempre *timezone-aware* em UTC, na persistência e nos esquemas.
- Separação de camadas, um pacote por camada:
  - `app/api/`: rotas; não acessam o banco nem contêm regra de negócio.
  - `app/services/`: regras de negócio, incluindo o `priority_advisor`; não conhecem HTTP.
  - `app/repositories/`: único ponto de acesso ao banco (engine, sessão e consultas); sem regra de negócio.
  - `app/models/`: modelos ORM, esquemas Pydantic e configurações; sem lógica.
  - `app/main.py`: apenas composição (criação da aplicação, `lifespan` e registro das rotas).
- Configuração só via pydantic-settings (`app/models/settings.py`); nenhum literal de configuração no código.
- Toda entrada e saída externa passa por esquemas Pydantic v2, com tipos, tamanhos máximos e `Literal`.
- Decisões de arquitetura ficam nos ADRs de `docs/arquitetura.md`, e decisões técnicas de implementação em `docs/decisoes.md` (ver [Decisões técnicas](#decisões-técnicas)). Segui-las; mudar só com nova decisão registrada no arquivo correspondente.
- Não adicionar funcionalidades, dependências, abstrações, diretórios ou arquivos de raiz além do escopo definido no README e da [Estrutura de diretórios](#estrutura-de-diretórios). Itens listados em "Limitações e Próximos Passos" são previsão futura, não meta do MVP; não antecipar código, dependências ou configuração para eles.

### Decisões técnicas

Toda escolha técnica feita durante a implementação que não esteja no *blueprint* nem nos ADRs, e que outra pessoa precisaria conhecer para manter o código, é registrada em `docs/decisoes.md`. Exemplos: forma de converter datas para UTC, padrão de tratamento de exceções, nomes de exceções de domínio, estrutura de uma *fixture*.

- O arquivo é criado com a primeira decisão registrada (não antes), com uma entrada por decisão, numerada `DT-NN`.
- Cada entrada traz: data e *release*; contexto (o problema); decisão; alternativas consideradas e por que foram descartadas; consequências; IDs relacionados (RF, RT, ADR).
- Limite com os ADRs: decisão que afeta camadas, dependências entre módulos, persistência ou contrato da API é ADR em `docs/arquitetura.md`; decisão local ao código é DT. Na dúvida, DT, e a revisão da `v0.5.0` promove a ADR o que for estrutural.
- A DT nasce no mesmo *commit* do código que a aplica.

### APIs deprecadas: roteiro de checagem

Não há lista fixa: o que é deprecado depende das versões instaladas. Antes de escrever o primeiro código de cada *release* que toque em FastAPI, Starlette, Pydantic, SQLAlchemy ou na biblioteca padrão, e sempre que uma versão mudar:

1. Ler as notas de versão oficiais das versões fixadas no `requirements.txt`.
2. Para cada padrão suspeito, escrever um teste mínimo e rodar `python -m pytest -W error`; o que emitir aviso ou falhar é proibido.
3. Registrar o resultado na tabela abaixo (padrão, substituto, versão em que foi verificado, data) e os detalhes em `docs/HISTORY-IA.md`.

Padrões suspeitos a checar primeiro, por serem os que assistentes de IA costumam gerar a partir de código antigo:

| Padrão suspeito | Substituto provável | Situação |
| --- | --- | --- |
| `@app.on_event("startup")` / `on_startup` | `FastAPI(lifespan=...)` com `@asynccontextmanager` | proibido (FastAPI 0.142.2, 04/10/2026): `DeprecationWarning`; `lifespan` permitido |
| `class Config:` em modelos Pydantic | `model_config = ConfigDict(...)` | proibido (Pydantic 2.13.5, 04/10/2026): `PydanticDeprecatedSince20`; `ConfigDict` permitido |
| `class Config:` em `BaseSettings` | `model_config = SettingsConfigDict(env_file=".env")` | proibido (pydantic-settings 2.15.0, 04/10/2026): `PydanticDeprecatedSince20`; `SettingsConfigDict` permitido |
| `datetime.utcnow()` | `datetime.now(datetime.UTC)` | proibido (Python 3.14.6, 04/10/2026): `DeprecationWarning`; `now(UTC)` permitido |
| `declarative_base()` | `class Base(DeclarativeBase)` | estilo legado, evitar (SQLAlchemy 2.1.3, 04/10/2026): sem aviso; `DeclarativeBase` permitido |
| cliente HTTP usado pelo `TestClient` (`httpx` vs. sucessor) | `httpx2` (2.13.1): sem ele, o Starlette recorre ao `httpx` e emite aviso de deprecação | proibido `httpx` (Starlette 1.7.0, 03/10/2026); `httpx2` permitido (04/10/2026) |
| fixture de banco em memória sem `engine.dispose()` | chamar `engine.dispose()` ao final da fixture | proibido (SQLAlchemy 2.1.3, Python 3.14.6, 04/10/2026): `ResourceWarning` (`unclosed database`) vira `PytestUnraisableExceptionWarning`; com `dispose()` permitido |
| `mypy app` sobre `app/` sem `__init__.py` na raiz | `python -m mypy --explicit-package-bases app` (ADR-11) | proibido `mypy app` (mypy 2.4.0, 04/10/2026): "Source file found twice under different module names"; com `--explicit-package-bases` permitido |

Situação possível: "proibido (vX.Y, dd/mm/aaaa)", "permitido (vX.Y, dd/mm/aaaa)" ou "estilo legado, evitar". Os testes mínimos da rodada de 04/10/2026 estão em `docs/release-review-010.md`.

## Testes

Três arquivos, um por alvo, sem `conftest.py`: cada fixture fica no arquivo de teste que a usa.

- `tests/test_task_service.py`: unitários do *service* de tarefas, isolando o *repository* com um dublê simples (não *mocks* elaborados).
- `tests/test_priority_advisor.py`: unitários do `priority_advisor`, funções puras, sem banco nem HTTP.
- `tests/test_task_routes.py`: integração de todos os endpoints, incluindo `/health`, com `TestClient` e SQLite em memória (`sqlite://` com `StaticPool`).
- Cobrir sucesso e erro de cada endpoint: tarefa inexistente, *status* ou prioridade inválidos, título vazio, campo acima do tamanho máximo, data/hora em formato inválido. Testar `/health` com banco indisponível e documentação indisponível com `ENVIRONMENT=production`.
- Fixtures liberam todos os recursos que abrem (conexões, *engines*); vazamento de recurso gera aviso e o `-W error` falha.
- Testes são reproduzíveis: rodam com `python -m pytest -W error` em máquina limpa, sem configuração manual, e não deixam arquivos no repositório (o `.pytest_cache` é ignorado pelo git).
- Novo arquivo de teste só com nova decisão registrada no *blueprint* e nesta seção.

## Segurança

- **SQL injection:** todo acesso ao banco via ORM ou consulta parametrizada. Nunca montar SQL por concatenação ou *f-string*. SQL textual só com `sqlalchemy.text()` e parâmetros nomeados.
- **Validação de entrada:** todo dado externo passa pelos esquemas Pydantic.
- **Credenciais e configuração:** só em variáveis de ambiente ou `.env` (nunca versionado); o README (Configuração) lista as variáveis sem valores sensíveis. Isso vale também para chaves de serviços externos que venham a existir no futuro.
- **Exposição de informações:** mensagens de erro não revelam detalhes internos (*stack traces*, SQL, caminhos); detalhes vão para o log. Documentação da API desabilitada em produção.

## Estrutura de diretórios

Estrutura alvo, fechada: os diretórios e os arquivos de raiz são exatamente estes. Os arquivos dentro dos pacotes de `app/` e de `docs/` são a proposta inicial e podem ser ajustados no *blueprint*, sem criar novos diretórios. Os arquivos são criados ao longo das *releases*; não criar arquivos vazios por antecipação.

```
laboratorio-projeto/
├── .pytest_cache/             # gerado pelo pytest (ignorado pelo git)
├── .venv/                     # ambiente virtual local (ignorado pelo git)
├── app/
│   ├── api/                   # controller
│   │   ├── __init__.py
│   │   ├── task_routes.py     # endpoints de tarefas
│   │   └── health_routes.py   # endpoint /health
│   ├── models/                # estruturas de dados, sem lógica
│   │   ├── __init__.py
│   │   ├── base.py            # Base declarativo do SQLAlchemy
│   │   ├── task.py            # modelo ORM da tarefa
│   │   ├── task_schemas.py    # esquemas Pydantic e tipos TaskStatus, TaskPriority
│   │   ├── health_schemas.py  # esquema HealthRead e tipo HealthStatus da resposta de /health
│   │   └── settings.py        # configurações lidas do ambiente/.env (pydantic-settings)
│   ├── repositories/          # acesso ao banco
│   │   ├── __init__.py
│   │   ├── database.py        # engine SQLite, sessão, dependência get_db e ping (SELECT 1)
│   │   └── task_repository.py # consultas e persistência de tarefas
│   ├── services/              # regras de negócio
│   │   ├── __init__.py
│   │   ├── task_service.py    # casos de uso de tarefas
│   │   ├── health_service.py  # verificação de saúde (chama database.ping)
│   │   └── priority_advisor.py # regras de prioridade (determinísticas, sem IA)
│   └── main.py                # criação da aplicação FastAPI, lifespan e registro das rotas
├── docs/
│   ├── arquitetura.md         # arquitetura, diagramas Mermaid.js e ADRs
│   ├── escopo-mvp.md          # objetivo, requisitos, fora de escopo e decisões em aberto
│   ├── backlog.md             # itens RF/RT por release, critérios de aceite e estimativas
│   ├── mermaid.md             # catálogo dos diagramas, com antes e depois de cada revisão
│   ├── requerimentos.md       # requisitos de entrega do curso
│   ├── PRE-HISTORY-IA.md      # uso de IA antes do repositório (concepção do CLAUDE.md)
│   ├── EXTRA-HISTORY-IA.md    # uso de IA em modo chat fora do repositório (registro do autor)
│   ├── HISTORY-IA.md          # histórico do uso de IA no projeto
│   ├── decisoes.md            # decisões técnicas de implementação (DT-NN)
│   ├── blueprint-vXYZ.md      # blueprint aprovado de cada release (ex.: blueprint-v020.md)
│   ├── release-review-010.md  # revisão de publicação da release v0.1.0
│   └── release-prompts-solon-020.md # prompts de exemplo do tutor do curso (referência)
├── prompts/
│   ├── Prompt NN - <título>   # um arquivo por prompt, numeração sequencial (00, 01, 02...)
│   └── prompts-desenvolvimento.md # índice dos prompts planejados para v0.2.0 a v1.0.0
├── tests/
│   ├── test_priority_advisor.py # unitários do priority_advisor
│   ├── test_task_routes.py    # integração dos endpoints (inclui /health)
│   └── test_task_service.py   # unitários do service de tarefas
├── .gitignore
├── CHANGELOG.md               # mudanças por release (Keep a Changelog)
├── LICENSE                    # licença MIT
├── README.md
├── requirements.txt           # dependências com versões fixadas
└── CLAUDE.md                  # este arquivo
```

## Ambiente de desenvolvimento

Windows 11 com PowerShell; o README traz os comandos em PowerShell e em Bash. Python 3.11 é o mínimo; registrar no README a versão em que o projeto foi testado. Diagramas em Mermaid.js, renderizados pelo próprio GitHub (sem dependência de Node.js).

Nesta máquina, o Smart App Control do Windows está ativo e bloqueia as extensões compiladas (`.pyd`, sem assinatura) do SQLAlchemy. O SQLAlchemy 2.1.3 do `.venv` foi reinstalado em Python puro, na mesma versão; o procedimento está no README (Solução de problemas).
