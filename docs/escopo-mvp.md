# Escopo do MVP

> **Status:** escopo definido após a *release* `v0.1.0`, antes do código da aplicação; decisões D-01 a D-04 incorporadas aos requisitos no fechamento da `v0.3.0` (06/10/2026). Vale como referência para os *blueprints* das *releases* `v0.2.0` a `v1.0.0`. Mudança de escopo só com pedido explícito do autor, registrada aqui e no [`CHANGELOG.md`](../CHANGELOG.md).

Este documento é a fonte de verdade dos requisitos do MVP: objetivo, requisitos funcionais e não funcionais, itens fora de escopo e decisões em aberto. O [`README.md`](../README.md) traz o resumo, o roadmap e as instruções de uso; a [`docs/arquitetura.md`](arquitetura.md) traz o desenho técnico e os ADRs; o [`docs/backlog.md`](backlog.md) desdobra os requisitos em itens por *release*, com critérios de aceite.

## 1. Objetivo

Entregar uma micro-API REST de gestão de tarefas (*To-Do List*) com prioridades, em Python, FastAPI e SQLite3, que um avaliador consiga clonar, instalar, executar e testar em uma máquina limpa, sem conhecimento prévio do projeto.

O MVP é o miniprojeto acadêmico do curso 1 da pós-graduação SWE-GENAI. O valor da entrega está tanto no produto (uma API pequena, correta e bem testada) quanto no processo (uso documentado de IA generativa em todo o ciclo de vida).

### 1.1 Critérios de sucesso

O MVP está concluído, na *release* `v1.0.0`, quando:

1. todos os requisitos funcionais da seção 3 estão implementados e cobertos por testes;
2. a definição de pronto passa em ambiente limpo, sem avisos:
   `python -m pytest -W error` (sem checagem de tipos por ferramenta, ADR-21);
3. o README permite instalar, executar e testar seguindo apenas os comandos documentados, em PowerShell e em Bash;
4. os requisitos de entrega do curso ([`docs/requerimentos.md`](requerimentos.md)) estão atendidos (seção 7);
5. a *tag* `v1.0.0` está publicada no GitHub.

### 1.2 Restrições

| Restrição | Valor |
| --- | --- |
| Orçamento | cerca de 30 horas |
| Uso | local, um único usuário, sem requisito de desempenho ou escala |
| *Stack* | Python 3.11+, FastAPI, SQLAlchemy, Pydantic v2, SQLite3; versões fixadas no [`requirements.txt`](../requirements.txt) |
| Plataforma de desenvolvimento | Windows 11 com PowerShell; comandos também documentados em Bash |
| Estrutura do repositório | fechada, definida no [`CLAUDE.md`](../CLAUDE.md) |

## 2. Conceitos

| Termo | Definição |
| --- | --- |
| Tarefa | unidade de trabalho com título, descrição opcional, *status*, prioridade e data/hora opcional |
| Tarefa aberta | tarefa sem data/hora estipulada (`due_at` vazio) |
| Tarefa específica | tarefa com data/hora estipulada (`due_at` preenchido) |
| Prioridade | inteiro de 1 a 4: 1 = mandatória (fazer imediatamente); 2 = importante (fazer hoje, se possível); 3 = regular (fazer quando houver tempo); 4 = agendada (fazer na data/hora estipulada). Prioridade 4 exige `due_at`; `due_at` não exige prioridade 4 (D-05) |
| Prioridade sugerida | prioridade calculada pelo `priority_advisor` a partir do tempo restante até `due_at` (até 4 h: 1; até 24 h: 2; até 7 dias: 3; acima: 4; limites na faixa mais urgente); `null` para tarefa aberta ou concluída. Devolvida em `suggested_priority`, nunca gravada e sem alterar a prioridade (D-07) |
| *Status* | situação da tarefa, de um conjunto fechado (`TaskStatus`): `pending` (pendente) ou `done` (concluída) (D-01) |
| `priority_advisor` | módulo de regras determinísticas de prioridade, sem IA, chamado pelo *service* |

### 2.1 Atributos da tarefa

| Atributo | Tipo | Regra |
| --- | --- | --- |
| `id` | inteiro | gerado pelo banco |
| `title` | texto | obrigatório, 1 a 200 caracteres, sem os espaços das pontas |
| `description` | texto | opcional, até 1000 caracteres |
| `status` | `TaskStatus` (`Literal["pending", "done"]`) | valor do conjunto fechado; padrão `pending` na criação (D-01) |
| `priority` | `TaskPriority` (`Literal[1, 2, 3, 4]`) | valor do conjunto fechado; padrão `3` na criação (D-04); coluna existente desde a `v0.3.0` (D-03); `4` exige `due_at` (D-05) |
| `due_at` | data/hora | opcional; entrada em `DD/MM/AAAA HH:MM` (horário local), `DD/MM/AAAA` (horário local, valendo até 23:59) ou ISO 8601 com fuso; armazenada em UTC e devolvida no fuso local de `LOCAL_UTC_OFFSET` (D-09) |
| `created_at` | data/hora | definida na criação; armazenada em UTC e devolvida no fuso local; somente leitura |
| `updated_at` | data/hora | atualizada a cada alteração; armazenada em UTC e devolvida no fuso local; somente leitura |
| `suggested_priority` | `TaskPriority` ou `null` | calculada a cada resposta, nunca gravada (D-07); somente leitura |

## 3. Requisitos funcionais

Cada requisito indica a *release* prevista no roadmap do README. Os códigos de resposta seguem o fluxo de dados de [`docs/arquitetura.md`](arquitetura.md) (seção 3). Toda entrada inválida (tipo, tamanho, valor fora do conjunto, data/hora mal formada) responde **422**; tarefa inexistente responde **404**; falha inesperada responde **500** com mensagem genérica.

| ID | Requisito | Critério de aceitação | *Release* |
| --- | --- | --- | --- |
| RF-01 | Criar tarefa | `POST /tasks` com corpo válido responde **201** com a tarefa criada, incluindo `id`, `created_at` e `updated_at`; título vazio ou acima de 200 caracteres, descrição acima de 1000, *status* ou prioridade fora do conjunto e data/hora inválida respondem **422** | `v0.3.0` |
| RF-02 | Listar tarefas | `GET /tasks` responde **200** com a lista de tarefas (vazia, se não houver) | `v0.3.0` |
| RF-03 | Filtrar a listagem por *status* | `GET /tasks?status=<valor>` devolve só as tarefas com aquele *status*; valor fora do conjunto responde **422** | `v0.3.0` |
| RF-04 | Consultar tarefa | `GET /tasks/{id}` responde **200** com a tarefa ou **404** se ela não existir | `v0.3.0` |
| RF-05 | Atualizar tarefa (total) | `PUT /tasks/{id}` substitui os campos editáveis, atualiza `updated_at` e responde **200**; **404** se não existir; **422** se o corpo for inválido | `v0.3.0` |
| RF-06 | Atualizar tarefa (parcial) | `PATCH /tasks/{id}` altera só os campos enviados, atualiza `updated_at` e responde **200**; **404** e **422** como no RF-05 | `v0.3.0` |
| RF-07 | Marcar tarefa como concluída | `POST /tasks/{id}/complete` muda o *status* para `done` e responde **200** com a tarefa; repetir a operação responde **200** sem nova gravação, e `updated_at` não muda (idempotente, D-02); **404** se não existir | `v0.3.0` |
| RF-08 | Excluir tarefa | `DELETE /tasks/{id}` responde **204** sem corpo; **404** se não existir | `v0.3.0` |
| RF-09 | Prioridade e tipo da tarefa | toda tarefa tem prioridade de 1 a 4 e pode ser aberta ou específica; `due_at` aceito em `DD/MM/AAAA HH:MM` (horário local), `DD/MM/AAAA` (23:59 local) ou ISO 8601 com fuso, e qualquer outro formato responde **422**; as datas da resposta vêm no fuso de `LOCAL_UTC_OFFSET`, e um valor de `LOCAL_UTC_OFFSET` fora de `±HH:MM` impede a partida (D-09) | `v0.4.0` |
| RF-10 | Validar coerência de prioridade | prioridade 4 sem `due_at` é recusada na criação, no `PUT` e no `PATCH` (no estado resultante) com **422** e `{"detail": "Prioridade 4 (agendada) exige due_at preenchido"}`, sem alterar a tarefa (D-05, ADR-17) | `v0.4.0` |
| RF-11 | Sugerir prioridade | toda resposta de tarefa traz `suggested_priority`, calculada pelo `priority_advisor` pela proximidade do prazo (seção 2), sem alterar nem gravar a prioridade (D-07, ADR-16, ADR-17) | `v0.4.0` |
| RF-12 | Verificar saúde | `GET /health` executa `SELECT 1` no banco e responde **200** se ele responder ou **503** se falhar, sem detalhes internos no corpo | `v0.2.0` |
| RF-13 | Documentação interativa da API | `/docs`, `/redoc` e `/openapi.json` disponíveis em `development` e `test`, e indisponíveis (**404**) com `ENVIRONMENT=production` | `v0.2.0` |
| RF-14 | Filtrar a listagem por prioridade | `GET /tasks?priority=<1 a 4>` devolve só as tarefas com aquela prioridade; combinado com `?status=`, devolve as que atendem aos dois; valor fora de 1 a 4 ou não inteiro responde **422** (D-06) | `v0.4.0` |

## 4. Requisitos não funcionais

| ID | Categoria | Requisito | Verificação |
| --- | --- | --- | --- |
| RNF-01 | Reprodutibilidade | o projeto é instalado, executado e testado em máquina limpa só com os comandos do README (Como rodar), em PowerShell e em Bash, com Python 3.11 ou superior | execução em clone limpo no fechamento de cada *release* |
| RNF-02 | Dependências | o `requirements.txt` é a única declaração de dependências, com versões fixadas e verificadas (fonte e data registradas) | `python -m pip check`; comparação com `pip freeze` |
| RNF-03 | Testabilidade | testes unitários do *service* e do `priority_advisor` e testes de integração de todos os endpoints, cobrindo sucesso e erro de cada um; banco em memória; sem estado local nem serviços externos | `python -m pytest -W error` |
| RNF-04 | Ausência de avisos | nenhum aviso de deprecação ou de recurso não liberado; padrões proibidos listados no roteiro de checagem do `CLAUDE.md` | `-W error` na definição de pronto |
| RNF-05 | Tipagem | *type hints* em todas as funções e retornos; conjuntos fechados com `typing.Literal` | revisão de código (mypy retirado em 07/10/2026, ADR-21) |
| RNF-06 | Arquitetura | camadas Controller → Service → Repository, um pacote por camada; rotas sem acesso ao banco nem regra de negócio; *service* sem conhecimento de HTTP (ADR-01) | revisão de código na `v0.5.0` |
| RNF-07 | Configuração | toda configuração vem do ambiente ou do `.env`, via pydantic-settings; nenhum literal de configuração no código; variáveis documentadas no README sem valores sensíveis | revisão de código; testes com `ENVIRONMENT=production` |
| RNF-08 | Segurança: entrada | todo dado externo passa por esquemas Pydantic v2 com tipos, tamanhos máximos e `Literal` | testes de 422 |
| RNF-09 | Segurança: banco | acesso ao banco só via ORM ou consulta parametrizada (`text()` com parâmetros nomeados); nenhuma montagem de SQL por concatenação | revisão de código na `v0.5.0` |
| RNF-10 | Segurança: exposição | respostas de erro sem *stack trace*, SQL ou caminhos; detalhes só no log; documentação desabilitada em produção; nenhum segredo versionado | testes de 500 e 503; varredura antes do *push* |
| RNF-11 | Datas | datas e horas *timezone-aware*: em UTC na persistência (ADR-10); na entrada e na saída da API, no fuso local de `LOCAL_UTC_OFFSET` (ADR-18, D-09) | testes de criação e leitura com fusos diferentes |
| RNF-12 | Observabilidade | `/health` reflete o estado real do banco, não só do processo (ADR-07) | teste com banco indisponível |
| RNF-13 | Documentação | README completo e atualizado no fechamento de cada *release*; arquitetura em Mermaid renderizada pelo GitHub; documentação, *docstrings* e mensagens em português; identificadores em inglês | revisão no fechamento de cada *release* |
| RNF-14 | Versionamento | *Conventional Commits* em português, uma *branch* por mudança, *merge* `--no-ff`, *tag* anotada por *release*, `CHANGELOG.md` no padrão Keep a Changelog | revisão do histórico no fechamento de cada *release* |
| RNF-15 | Rastreabilidade do uso de IA | cada *prompt* registrado em `prompts/`; cada interação relevante registrada em `docs/HISTORY-IA.md`; assistentes e modelos listados no README | revisão no fechamento de cada *release* |

## 5. Fora de escopo

### 5.1 Previsões futuras

Possibilidades de evolução, listadas no README (Limitações e próximos passos). Não são meta do MVP: nenhum código, dependência ou configuração é antecipado para elas.

| Item | Motivo de ficar fora do MVP |
| --- | --- |
| Autenticação e usuários | o MVP é de uso local e de um único usuário; exigiria modelo de usuário, gestão de credenciais e testes de autorização |
| Paginação na listagem | volume de dados de uso pessoal não a justifica no orçamento |
| *Frontend* | o entregável é a API; a documentação interativa cobre a interação manual |
| Migrações de banco com Alembic | o esquema é criado com `create_all` (ADR-05); sem dados de produção a preservar |
| Priorização assistida por IA (agente via API Claude) | depende de serviço externo e credenciais, e os testes não podem depender de serviços externos; o `priority_advisor` do MVP é determinístico |

### 5.2 Excluídos sem previsão

Itens que não fazem parte do MVP nem das previsões futuras. Pedido para qualquer um deles é ampliação de escopo e exige decisão explícita do autor.

- *Deploy* em servidor ou nuvem, contêineres e integração contínua.
- Banco de dados diferente do SQLite3 e acesso assíncrono ao banco.
- Busca textual, ordenação configurável e filtros além dos previstos (RF-03 e RF-14).
- Notificações e lembretes de prazo, tarefas recorrentes, subtarefas, categorias, etiquetas e anexos.
- Exclusão lógica, histórico de alterações e auditoria.
- Limitação de taxa (*rate limiting*), CORS configurável e HTTPS na própria aplicação.
- Requisitos de desempenho, escala e concorrência entre múltiplos usuários.
- Internacionalização das mensagens da API.

## 6. Decisões em aberto

Decisões deixadas para o *blueprint* da *release* indicada. A recomendação é do assistente; a decisão é do autor. Ao serem tomadas, saem desta seção e vão para o requisito correspondente ou para um ADR de [`docs/arquitetura.md`](arquitetura.md).

| # | Decisão | Recomendação | *Release* |
| --- | --- | --- | --- |
| D-01 | Valores de `TaskStatus` | **Decidida** em 05/10/2026, conforme a recomendação: `pending` e `done`, padrão `pending`. Migrada para a seção 2 (Conceitos e atributos) e para o ADR-15 | `v0.3.0` |
| D-02 | Rota da marcação como concluída (RF-07) | **Decidida** em 05/10/2026, conforme a recomendação: `POST /tasks/{id}/complete`, idempotente. Migrada para o RF-07 e para o ADR-15 | `v0.3.0` |
| D-03 | Coluna `priority` criada já na `v0.3.0` ou só na `v0.4.0` | **Decidida** em 05/10/2026, conforme a recomendação: coluna criada na `v0.3.0`, sem migrações (ADR-05); as regras ficam na `v0.4.0`. Migrada para a seção 2.1 | `v0.3.0` |
| D-04 | Prioridade padrão | **Decidida** em 05/10/2026, conforme a recomendação: `3` (regular), aplicada pelo esquema de criação. Migrada para a seção 2.1 | `v0.3.0` |
| D-05 | Prioridade 4 exige data/hora, e data/hora exige prioridade 4 | **Decidida** em 06/10/2026, conforme a recomendação: prioridade 4 exige `due_at`; `due_at` não exige prioridade 4; no `PATCH`, conferida no estado resultante. Migrada para a seção 2, o RF-10 e o ADR-17 | `v0.4.0` |
| D-06 | Filtro da listagem por prioridade | **Decidida** em 06/10/2026: incluído como RF-14, pelas horas reais frente ao orçamento ([`docs/blueprint-v040.md`](blueprint-v040.md), seção 2.1). Migrada para o RF-14 e o ADR-17 | `v0.4.0` |
| D-07 | Regras e exposição do `priority_advisor` (RF-10 e RF-11) | **Decidida** em 06/10/2026, conforme a recomendação: coerência na criação e na atualização; sugestão no campo calculado `suggested_priority`, sem alterar nem gravar a prioridade. Migrada para a seção 2, o RF-11 e os ADR-16 e ADR-17 | `v0.4.0` |
| D-08 | Esquema Pydantic da resposta de `/health` e arquivo onde fica | **Decidida** em 05/10/2026: novo `app/models/health_schemas.py`, separado dos esquemas de tarefa, com o modelo `HealthRead` (`status` e `database`, ambos `ok` ou `unavailable`); contrato no ADR-13 de [`docs/arquitetura.md`](arquitetura.md) e em [`docs/blueprint-v020.md`](blueprint-v020.md). Levantada na revisão dos diagramas (Prompt 12) | `v0.2.0` |
| D-09 | Datas no horário local, para preenchimento por pessoas | **Decidida** em 06/10/2026, a pedido do autor na revisão do *blueprint* da `v0.4.0`: `due_at` aceito em `DD/MM/AAAA HH:MM` e `DD/MM/AAAA` (23:59) no horário local, além de ISO 8601 com fuso; datas devolvidas no fuso local; fuso fixo em `LOCAL_UTC_OFFSET` (padrão `-03:00`); persistência em UTC. Migrada para a seção 2.1, o RF-09, o RNF-11 e o ADR-18 | `v0.4.0` |

A decisão D-08 foi tomada no [`docs/blueprint-v020.md`](blueprint-v020.md) (seção 2), as decisões D-01 a D-04 no [`docs/blueprint-v030.md`](blueprint-v030.md) (seção 2.1), e D-05 a D-07 e D-09 no [`docs/blueprint-v040.md`](blueprint-v040.md) (seção 2.1), todas confirmadas na aprovação do autor. Ficam na tabela, marcadas como decididas, para manter a rastreabilidade; o conteúdo vigente está nos requisitos e ADRs indicados. Não há decisão em aberto.

## 7. Rastreabilidade com os requisitos de entrega do curso

| Requisito de [`docs/requerimentos.md`](requerimentos.md) | Atendido por | Situação |
| --- | --- | --- |
| Repositório público, sem informações sensíveis | repositório no GitHub; `.env` ignorado; RNF-07 e RNF-10 | atendido desde a `v0.1.0` |
| Histórico de *commits* consistente (*Conventional Commits*) | RNF-14; `CHANGELOG.md` | em andamento |
| README: título, descrição, configuração, como rodar | README (Objetivo, Configuração, Como rodar) | atendido; revisado a cada *release* |
| README: exemplos de uso da API | README (Endpoints) | atendido na `v0.3.0`: exemplos executados na API em PowerShell e Bash; ampliado na `v0.4.0` com prioridade, sugestão, filtro e datas no horário local |
| README: tecnologias, modelos de IA e assistentes | README (Stack e Uso de IA generativa); RNF-15 | atendido |
| README: limitações e próximos passos | README (Limitações e próximos passos); seção 5 deste documento | atendido |
| README: créditos e licença | README (Créditos e licença); `LICENSE` | atendido |
| Gerenciamento de dependências | `requirements.txt`; RNF-02 | atendido |
| Testes automatizados executáveis e passando | RNF-03 e RNF-04 | em andamento: 13 testes na `v0.2.0`, 69 na `v0.3.0` e 134 na `v0.4.0` (com `tests/test_priority_advisor.py`), todos passando com `-W error`; revisão final na `v0.5.0` |
| *Release* ou *tag* de entrega | *tag* e *release* `v1.0.0`; RNF-14 | pendente |
