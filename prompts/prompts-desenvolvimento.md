# Prompts de desenvolvimento: `v0.2.0` a `v1.0.0`

> **Status:** executado (Prompts 21 a 43 de 05 a 07/10/2026; o Prompt 44 publica a `v1.0.0`). Proposto no Prompt 20 (05/10/2026). O mypy citado nos *prompts* foi retirado do projeto pelo ADR-21 (07/10/2026); a definição de pronto passou a ser só `python -m pytest -W error`. Os textos dos *prompts* abaixo não mudaram. Adaptação dos *prompts* de exemplo do tutor ([`docs/release-prompts-solon-020.md`](../docs/release-prompts-solon-020.md)) ao processo deste projeto. Depois de aprovado, cada *prompt* abaixo vira um arquivo `prompts/Prompt NN - <título>` no momento do uso, e este arquivo passa a ser o índice da fase de desenvolvimento.

## Como usar

- **Numeração.** Continua a sequência de `prompts/` (o último é o Prompt 20). Os números 21 a 44 abaixo são os nomes dos arquivos a criar; a ordem é a de execução.
- **Campos.** Como no exemplo do tutor: Contexto, Objetivo, Estilo e Resposta. O que vale para todos os *prompts* não é repetido no texto: ler o `CLAUDE.md` e a fonte de verdade citada; *branch* a partir de `main`; código e testes juntos; definição de pronto (`python -m pytest -W error` e `python -m mypy --explicit-package-bases app`) ao fim de cada passo; *commit* e *push* só quando pedidos; registro da execução no arquivo do *prompt* e em `docs/HISTORY-IA.md`.
- **Diferença em relação ao exemplo do tutor.** O tutor pede um arquivo de código por *prompt*, sem plano prévio. Aqui cada *release* tem um *blueprint* executável aprovado antes do código (`CLAUDE.md`, Blueprint executável); os *prompts* de código executam passos desse *blueprint*, agrupados por item do backlog, e cada *release* termina com um *prompt* de fechamento. Os passos exatos são numerados no *blueprint*; por isso os *prompts* de execução citam os itens (RT/RF) e não números de passo.
- **Modelo sugerido.** *Blueprints*, revisões e fechamentos com o modelo de planejamento (Claude Opus 5.5 ou Claude Fable 5.1). Execução dos passos do *blueprint* com o Claude Sonnet 5.5, como prevê o `CLAUDE.md`. Se um passo de execução falhar de forma não prevista, o modelo para e reporta; a correção volta ao modelo de planejamento.
- **Granularidade.** Um *prompt* de execução pode ser dividido em vários, um por passo do *blueprint*, se a *release* ficar grande. O inverso (juntar *prompts*) não é recomendado: a revisão humana entre eles é o ponto de controle.

## Resumo

| Prompt | *Release* | Título | Itens | Tipo |
| --- | --- | --- | --- | --- |
| 21 | `v0.2.0` | blueprint da v0.2.0 | RT-01 a RT-04, RF-12, RF-13, D-08 | planejamento |
| 22 | `v0.2.0` | configuração e acesso ao banco | RT-01, RT-02 | execução |
| 23 | `v0.2.0` | aplicação, health e testes de integração | RT-03, RT-04, RF-12, RF-13 | execução |
| 24 | `v0.2.0` | fechamento da v0.2.0 | 2.1 do backlog | fechamento |
| 25 | `v0.3.0` | blueprint da v0.3.0 | RT-05 a RT-09, RF-01 a RF-08, D-01 a D-04 | planejamento |
| 26 | `v0.3.0` | modelo ORM e esquemas Pydantic | RT-05, RT-06 | execução |
| 27 | `v0.3.0` | repository de tarefas | RT-07 | execução |
| 28 | `v0.3.0` | service de tarefas e testes unitários | RT-08 | execução |
| 29 | `v0.3.0` | rotas CRUD e tratamento de erros | RT-09, RF-01 a RF-08 | execução |
| 30 | `v0.3.0` | documentação dos endpoints | RT-09 (critério 3) | documentação |
| 31 | `v0.3.0` | fechamento da v0.3.0 | 2.1 do backlog | fechamento |
| 32 | `v0.4.0` | blueprint da v0.4.0 | RT-10, RF-09 a RF-11, D-05 a D-07 | planejamento |
| 33 | `v0.4.0` | priority_advisor com funções puras | RT-10 | execução |
| 34 | `v0.4.0` | prioridades no service e nas rotas | RF-09, RF-10, RF-11, RF-14 (se aprovado) | execução |
| 35 | `v0.4.0` | fechamento da v0.4.0 | 2.1 do backlog | fechamento |
| 36 | `v0.5.0` | blueprint da v0.5.0 | RT-11 a RT-14 | planejamento |
| 37 | `v0.5.0` | revisão de arquitetura | RT-11 | revisão |
| 38 | `v0.5.0` | revisão de segurança | RT-12 | revisão |
| 39 | `v0.5.0` | revisão da documentação e das dependências | RT-13, RT-14 | revisão |
| 40 | `v0.5.0` | fechamento da v0.5.0 | 2.1 do backlog | fechamento |
| 41 | `v1.0.0` | blueprint da v1.0.0 | RT-15 a RT-17 | planejamento |
| 42 | `v1.0.0` | validação em máquina limpa | RT-15 | verificação |
| 43 | `v1.0.0` | consolidação do histórico de uso de IA | RT-16 | documentação |
| 44 | `v1.0.0` | publicação da entrega | RT-17 | fechamento |

*Branches*: `feat/base-tecnica` (21 a 24), `feat/crud-tarefas` (25 a 31), `feat/priority-advisor` (32 a 35), `refactor/revisao-v050` (36 a 40), `docs/entrega-v100` (41 a 44).

## `v0.2.0`: base técnica (4 h no backlog)

### Prompt 21 - blueprint da v0.2.0

```text
Contexto: Release v0.2.0 (base técnica) do docs/backlog.md: RT-01 a RT-04, RF-12 e RF-13. Decisão em aberto D-08 (esquema da resposta de /health e arquivo onde fica). É o primeiro código do projeto; o roteiro de checagem de APIs deprecadas do CLAUDE.md já está preenchido para as versões do requirements.txt.
Objetivo: Escrever docs/blueprint-v020.md conforme a seção "Blueprint executável" do CLAUDE.md: D-08 tomada no texto com a recomendação do escopo (novo app/models/health_schemas.py), a confirmar na aprovação; passos numerados com arquivos, assinaturas tipadas, regra de comportamento, testes nomeados por arquivo, comando de verificação e IDs (RT, RF, ADR); imports permitidos e padrões proibidos do roteiro de checagem; lista do que não fazer; estimativa frente às 4 h do backlog.
Estilo: Sem decisões em aberto; trechos de código só nos pontos sensíveis (SettingsConfigDict, lifespan com @asynccontextmanager, fixture com sqlite:// + StaticPool e engine.dispose()).
Resposta: Apenas o arquivo docs/blueprint-v020.md, para aprovação; nenhum código em app/ ou tests/. Git: branch feat/base-tecnica a partir de main; adicionar o arquivo; não comitar.
```

### Prompt 22 - configuração e acesso ao banco

```text
Contexto: docs/blueprint-v020.md aprovado. Itens RT-01 e RT-02; ADR-02, ADR-04 e ADR-07.
Objetivo: Executar os passos do blueprint que criam app/models/settings.py (Settings com DATABASE_URL e ENVIRONMENT tipada com Literal["development", "test", "production"], SettingsConfigDict com env_file), app/models/base.py (class Base(DeclarativeBase)) e app/repositories/database.py (engine a partir de DATABASE_URL com check_same_thread=False; fábrica de sessões; get_db abre uma sessão por requisição e a fecha ao final, inclusive em erro; ping(session) executa SELECT 1 via text() e devolve False em SQLAlchemyError, registrando o detalhe no log), com os __init__.py dos pacotes e os testes previstos no blueprint para esses passos.
Estilo: Python tipado, docstrings em português, nenhum literal de configuração fora de settings.py; sem class Config nem on_event.
Resposta: Código dos arquivos e dos testes; saída da definição de pronto. Parar e reportar se um passo falhar de forma não prevista no blueprint.
```

### Prompt 23 - aplicação, health e testes de integração

```text
Contexto: settings.py, base.py e database.py prontos. Itens RT-03, RT-04, RF-12 e RF-13; ADR-05 a ADR-09; D-08 conforme o blueprint.
Objetivo: Executar os passos do blueprint que criam app/models/health_schemas.py, app/services/health_service.py, app/api/health_routes.py e app/main.py (FastAPI com lifespan em @asynccontextmanager, Base.metadata.create_all no lifespan, documentação desabilitada com ENVIRONMENT=production, registro das rotas), e tests/test_task_routes.py com a fixture de banco em memória (sqlite:// com StaticPool, dependency_overrides de get_db, engine.dispose() e limpeza dos overrides ao final) e os testes: /health 200 com banco disponível e 503 com ping falhando, corpo sem SQL, caminho nem stack trace; /docs e /openapi.json 200 em development e 404 com /redoc em production; padrões de DATABASE_URL e ENVIRONMENT; ENVIRONMENT fora do conjunto impede a inicialização.
Estilo: Rotas sem acesso ao banco; service sem HTTP; TestClient com httpx2; nenhum arquivo criado pelos testes (git status limpo).
Resposta: Código dos arquivos e dos testes; saída de python -m pytest -W error e de python -m mypy --explicit-package-bases app; confirmação de que python -m uvicorn app.main:app --reload sobe a API a partir da raiz.
```

### Prompt 24 - fechamento da v0.2.0

```text
Contexto: Todos os passos de docs/blueprint-v020.md executados com a definição de pronto verde na branch feat/base-tecnica.
Objetivo: Aplicar a seção "Fechamento de release" do CLAUDE.md: README revisado por inteiro (status, roadmap com a v0.2.0 concluída, endpoint /health, Configuração, Como rodar, Uso de IA generativa); docs/arquitetura.md ajustada no que a implementação divergiu; docs/decisoes.md com as DTs surgidas (criar só se houver a primeira); docs/backlog.md com RT-01 a RT-04, RF-12 e RF-13 concluídos e as horas reais; CHANGELOG.md com a seção 0.2.0 agrupada por tipo de commit; docs/HISTORY-IA.md com as entradas dos Prompts 21 a 24 e a consolidação da release; remoção da seção "Ponto de partida" do CLAUDE.md.
Estilo: README descreve o projeto como ele está, não como foi planejado; divergências do blueprint listadas explicitamente.
Resposta: Lista dos arquivos alterados e das divergências. Git, após minha aprovação do fechamento: commits no padrão Conventional Commits na branch, merge --no-ff em main, tag anotada v0.2.0 e push; em seguida, definição de pronto em clone limpo.
```

## `v0.3.0`: CRUD de tarefas (6,5 h no backlog)

### Prompt 25 - blueprint da v0.3.0

```text
Contexto: Release v0.3.0 (CRUD de tarefas) do backlog: RT-05 a RT-09 e RF-01 a RF-08. Decisões em aberto D-01 a D-04 (docs/escopo-mvp.md, seção 6). Base técnica da v0.2.0 em main; fluxos de dados e modelo de dados em docs/arquitetura.md (seções 3 e 4).
Objetivo: Escrever docs/blueprint-v030.md conforme "Blueprint executável": D-01 (TaskStatus = pending e done), D-02 (POST /tasks/{id}/complete, idempotente), D-03 (coluna priority já nesta release) e D-04 (prioridade padrão 3) tomadas no texto com a recomendação do escopo, a confirmar na aprovação; modelo ORM Task com as colunas da seção 4; esquemas de criação, atualização total, atualização parcial e leitura (TaskCreate e TaskRead como na arquitetura; os demais nomeados no blueprint) com title de 1 a 200, description até 1000 e Literal; tratamento dos campos somente leitura na entrada; nome da exceção de domínio de tarefa inexistente; conversão de datas para UTC na escrita e na leitura (ADR-10); commit seguido de refresh no repository (ADR-12); tradução da exceção para 404 e da falha inesperada do banco para 500 com mensagem genérica; passos, testes nomeados por arquivo e estimativa frente às 6,5 h.
Estilo: Sem decisões em aberto; código só nos pontos sensíveis (conversão UTC, handler de exceção de domínio, handler de 500, dublê do repository).
Resposta: Apenas docs/blueprint-v030.md, para aprovação. Git: branch feat/crud-tarefas a partir de main; adicionar; não comitar.
```

### Prompt 26 - modelo ORM e esquemas Pydantic

```text
Contexto: docs/blueprint-v030.md aprovado. Itens RT-05 e RT-06; ADR-02 e ADR-10.
Objetivo: Executar os passos do blueprint que criam app/models/task.py (Task com Mapped e mapped_column: id, title, description, status, priority, due_at, created_at e updated_at; datas em UTC; updated_at muda a cada alteração; datas lidas do SQLite voltam timezone-aware) e app/models/task_schemas.py (TaskStatus e TaskPriority como Literal; esquemas de criação, atualização total, parcial e leitura com os limites de tamanho; leitura com ConfigDict(from_attributes=True); campos somente leitura tratados como o blueprint define), com os testes previstos para esses passos.
Estilo: Pydantic v2 e SQLAlchemy 2 declarativo; sem class Config nem datetime.utcnow(); docstrings em português; modelos sem lógica.
Resposta: Código dos arquivos, testes do passo e saída da definição de pronto.
```

### Prompt 27 - repository de tarefas

```text
Contexto: Modelo e esquemas prontos. Item RT-07; ADR-12.
Objetivo: Executar o passo do blueprint que cria app/repositories/task_repository.py com as funções de inserir, buscar por id, listar com filtro opcional por status, atualizar e excluir, todas recebendo a sessão como parâmetro; escritas confirmadas com commit seguido de refresh; buscar devolve None quando não há linha; get_db não faz commit.
Estilo: Só ORM ou text() com parâmetros nomeados; nenhuma concatenação de SQL; sem regra de negócio; assinaturas exatamente como no blueprint.
Resposta: Código do arquivo, testes previstos para o passo e saída da definição de pronto.
```

### Prompt 28 - service de tarefas e testes unitários

```text
Contexto: Repository pronto. Item RT-08; ADR-01.
Objetivo: Executar os passos do blueprint que criam app/services/task_service.py (casos de uso criar, listar com filtro, consultar, atualizar total, atualizar parcial, concluir e excluir; tarefa inexistente sinalizada pela exceção de domínio do blueprint, sem código HTTP; conversão do esquema de entrada em Task) e tests/test_task_service.py (dublê simples do repository em memória, sem banco; sucesso e tarefa inexistente de cada caso de uso; concluir idempotente; atualização parcial preserva os campos não enviados).
Estilo: Service sem importar FastAPI nem Starlette; dublê como classe simples, sem biblioteca de mocks; funções coesas, uma por caso de uso.
Resposta: Código dos arquivos e saída da definição de pronto.
```

### Prompt 29 - rotas CRUD e tratamento de erros

```text
Contexto: Service pronto. Itens RT-09 e RF-01 a RF-08; D-02; fluxos da seção 3 de docs/arquitetura.md.
Objetivo: Executar os passos do blueprint que criam app/api/task_routes.py (POST /tasks 201; GET /tasks com status opcional; GET, PUT, PATCH e DELETE /tasks/{id}; POST /tasks/{id}/complete; response_model com o esquema de leitura; sessão por Depends(get_db) apenas repassada ao service), registram o router em app/main.py, traduzem a exceção de domínio para 404 e a falha inesperada do banco para 500 com mensagem genérica e detalhe no log, e acrescentam a tests/test_task_routes.py os testes de sucesso e erro de cada endpoint: 201 com id, created_at, updated_at, status e prioridade padrão; 422 para título vazio ou acima de 200, descrição acima de 1000, status ou prioridade fora do conjunto e data/hora mal formada; lista vazia, completa e filtrada por status, com 422 para status inválido; 404 em todos os /tasks/{id}; PUT substitui os campos e altera updated_at, 422 para corpo incompleto; PATCH preserva os campos não enviados; complete idempotente; DELETE 204 e 404 na consulta seguinte; 500 com corpo genérico.
Estilo: Rotas sem acesso ao banco nem regra de negócio; códigos de resposta declarados nas rotas; mensagens de erro sem detalhes internos.
Resposta: Código dos arquivos, testes e saída da definição de pronto.
```

### Prompt 30 - documentação dos endpoints

```text
Contexto: CRUD implementado e testado na branch feat/crud-tarefas; o README ainda não tem a seção Endpoints (RT-09, critério 3; requisito do curso: exemplos de uso da API).
Objetivo: Escrever no README a seção Endpoints: tabela com método, rota, códigos de resposta e descrição; um exemplo de requisição e resposta por endpoint, obtido da API em execução, no mesmo padrão de Como rodar (PowerShell e Bash), incluindo um caso 404 e um 422; a tabela de /health da v0.2.0 integrada à mesma seção.
Estilo: Exemplos executados, não inventados; JSON real das respostas; sem alterar código.
Resposta: Seção Endpoints do README e a lista dos comandos executados para obtê-la.
```

### Prompt 31 - fechamento da v0.3.0

```text
Contexto: Todos os passos de docs/blueprint-v030.md executados e README (Endpoints) escrito, com a definição de pronto verde.
Objetivo: Aplicar "Fechamento de release" do CLAUDE.md: README por inteiro (status, roadmap com a v0.3.0 concluída, Endpoints, Uso de IA generativa); docs/escopo-mvp.md com D-01 a D-04 migradas da seção 6 para os requisitos ou ADRs; docs/arquitetura.md com o modelo de dados sem "padrão em aberto", ADRs novos e ajustes do que divergiu, com docs/mermaid.md atualizado se um diagrama mudar; docs/decisoes.md com as DTs; docs/backlog.md com RT-05 a RT-09 e RF-01 a RF-08 concluídos e horas reais; CHANGELOG.md com a seção 0.3.0; docs/HISTORY-IA.md com os Prompts 25 a 31 e a consolidação da release.
Estilo: README como o projeto está; divergências do blueprint listadas.
Resposta: Lista dos arquivos alterados e das divergências. Git, após minha aprovação: commits, merge --no-ff em main, tag anotada v0.3.0 e push; definição de pronto em clone limpo.
```

## `v0.4.0`: prioridades e `priority_advisor` (3,5 h no backlog)

### Prompt 32 - blueprint da v0.4.0

```text
Contexto: Release v0.4.0 (prioridades e priority_advisor) do backlog: RT-10 e RF-09 a RF-11; decisões em aberto D-05 a D-07; item condicionado RF-14 (filtro por prioridade, D-06). Horas reais das releases anteriores registradas no backlog.
Objetivo: Escrever docs/blueprint-v040.md: D-05 (prioridade 4 exige due_at; due_at não exige prioridade 4), D-06 (incluir ou não RF-14, decidido no texto a partir das horas reais frente ao orçamento) e D-07 (validação de coerência na criação e na atualização; sugestão por proximidade do prazo como campo calculado na resposta, sem alterar a prioridade gravada) tomadas com a recomendação do escopo, a confirmar na aprovação; regras de sugestão em tabela com as faixas de prazo em números; assinaturas das funções puras do advisor recebendo a data/hora de referência como parâmetro; nome da exceção de domínio de prioridade incoerente e sua tradução para 422 com mensagem clara; passos, testes nomeados (test_priority_advisor.py, test_task_service.py, test_task_routes.py) e estimativa frente às 3,5 h.
Estilo: Sem decisões em aberto; sem IA nem serviço externo no advisor; sem alterar o esquema do banco além do que create_all cria.
Resposta: Apenas docs/blueprint-v040.md, para aprovação. Git: branch feat/priority-advisor a partir de main; adicionar; não comitar.
```

### Prompt 33 - priority_advisor com funções puras

```text
Contexto: docs/blueprint-v040.md aprovado. Item RT-10; regras de RF-10 e RF-11 conforme o blueprint.
Objetivo: Executar os passos do blueprint que criam app/services/priority_advisor.py (funções puras: validar a coerência entre prioridade e due_at conforme D-05, levantando a exceção de domínio do blueprint; sugerir prioridade pela proximidade do prazo a partir de uma data/hora de referência recebida como parâmetro, pela tabela do blueprint) e tests/test_priority_advisor.py (cada regra e seus limites exatos; tarefa aberta sem prazo; prazo no passado; due_at com fuso diferente de UTC; combinações coerentes e incoerentes).
Estilo: Sem importar banco, repository, FastAPI, nem chamar datetime.now() dentro das regras; tipos TaskPriority de task_schemas; docstrings com a regra em português.
Resposta: Código dos arquivos e saída da definição de pronto.
```

### Prompt 34 - prioridades no service e nas rotas

```text
Contexto: Advisor pronto. Itens RF-09, RF-10, RF-11 e, se aprovado em D-06, RF-14; ADR-10.
Objetivo: Executar os passos do blueprint que integram o advisor ao task_service (validação de coerência na criação, no PUT e no PATCH; sugestão calculada na resposta conforme D-07), ajustam os esquemas (prioridade 1 a 4 na entrada; campo de sugestão na leitura) e as rotas (422 com mensagem clara para incoerência; filtro por prioridade em GET /tasks se RF-14 aprovado), e acrescentam os testes: unitários em test_task_service.py (service chama o advisor; incoerência levanta a exceção) e de integração em test_task_routes.py (prioridade fora do conjunto 422; tarefa aberta e específica persistidas e devolvidas; due_at com fuso diferente devolvido em UTC; combinação incoerente 422 em POST, PUT e PATCH; sugestão presente e prioridade gravada inalterada; filtro por prioridade válido e inválido, se RF-14).
Estilo: Regra só no service e no advisor; rotas apenas traduzem a exceção; README (Endpoints) atualizado com a sugestão e, se houver, o filtro.
Resposta: Código dos arquivos alterados, testes, seção do README e saída da definição de pronto.
```

### Prompt 35 - fechamento da v0.4.0

```text
Contexto: Todos os passos de docs/blueprint-v040.md executados com a definição de pronto verde. Com a v0.4.0, todos os requisitos funcionais do escopo estão implementados.
Objetivo: Aplicar "Fechamento de release" do CLAUDE.md: README por inteiro (status, roadmap, Endpoints com prioridade e sugestão, Uso de IA generativa); docs/escopo-mvp.md com D-05 a D-07 migradas e RF-14 incluído ou registrado como não aprovado; docs/arquitetura.md ajustada (fluxo de POST /tasks com a sugestão, se mudar) e docs/mermaid.md se um diagrama mudar; docs/decisoes.md; docs/backlog.md com RT-10 e RF-09 a RF-11 (e RF-14) concluídos e horas reais; CHANGELOG.md com a seção 0.4.0; docs/HISTORY-IA.md com os Prompts 32 a 35 e a consolidação.
Estilo: README como o projeto está; divergências do blueprint listadas.
Resposta: Lista dos arquivos alterados e das divergências. Git, após minha aprovação: commits, merge --no-ff em main, tag anotada v0.4.0 e push; definição de pronto em clone limpo.
```

## `v0.5.0`: revisão de arquitetura, segurança e documentação (2,5 h no backlog)

### Prompt 36 - blueprint da v0.5.0

```text
Contexto: Release v0.5.0 (revisão) do backlog: RT-11 a RT-14. Código completo das releases v0.2.0 a v0.4.0 em main; DTs em docs/decisoes.md; horas reais acumuladas no backlog.
Objetivo: Escrever docs/blueprint-v050.md: ordem das revisões (arquitetura, segurança, documentação e dependências), critérios de aceite de cada uma copiados do backlog, forma do checklist de cada revisão (arquivo, linha, desvio, evidência, ação), regra de decisão para corrigir no código ou registrar em documento, critério para promover uma DT a ADR, limites do que pode ser alterado (sem funcionalidade nova, sem dependência nova) e estimativa frente às 2,5 h.
Estilo: Blueprint curto; sem decisões em aberto; sem código.
Resposta: Apenas docs/blueprint-v050.md, para aprovação. Git: branch refactor/revisao-v050 a partir de main; adicionar; não comitar.
```

### Prompt 37 - revisão de arquitetura

```text
Contexto: docs/blueprint-v050.md aprovado. Item RT-11; diagrama de módulos de docs/arquitetura.md (seção 2) e DTs de docs/decisoes.md.
Objetivo: Conferir cada import de app/ contra o diagrama de módulos: nenhuma dependência para cima (rotas sem repository nem banco; services sem FastAPI ou Starlette; repositories sem services; models sem lógica; main.py só composição); funções com mais de uma responsabilidade ou acima de cerca de 30 linhas; conjuntos fechados sem Literal; nomes fora da nomenclatura semântica. Corrigir no código o que for desvio; registrar em docs/arquitetura.md (ajuste pontual ou novo ADR) o que for decisão; promover a ADR as DTs estruturais; atualizar docs/mermaid.md se um diagrama mudar.
Estilo: Checklist com arquivo, linha, desvio e ação tomada; sem refatoração além dos desvios encontrados; testes existentes continuam passando sem alteração de comportamento.
Resposta: Checklist, diffs aplicados e saída da definição de pronto.
```

### Prompt 38 - revisão de segurança

```text
Contexto: Item RT-12; seção Segurança do CLAUDE.md; RNF-08 a RNF-10.
Objetivo: Verificar e corrigir: nenhum SQL por concatenação ou f-string (busca por text(, execute( e strings formatadas em app/); toda entrada passando por esquemas Pydantic com limites e Literal, inclusive parâmetros de consulta e de rota; respostas 404, 422, 500 e 503 sem stack trace, SQL ou caminho, com os testes existentes conferidos e completados; documentação desabilitada em production confirmada por teste; varredura de segredos nos arquivos e no histórico (git log -p com padrões de chave, token e senha; .env ausente do repositório); logs sem dados sensíveis.
Estilo: Checklist com evidência (comando executado e resultado) para cada item; correções mínimas; nenhuma dependência nova.
Resposta: Checklist, diffs aplicados, testes acrescentados e saída da definição de pronto.
```

### Prompt 39 - revisão da documentação e das dependências

```text
Contexto: Itens RT-13 e RT-14; README, docs/escopo-mvp.md, requirements.txt e o roteiro de checagem de APIs deprecadas do CLAUDE.md.
Objetivo: (1) Documentação: executar todos os exemplos do README (Endpoints) contra a API em execução e corrigir divergências; conferir Configuração e Como rodar em PowerShell; docstrings em todas as classes e funções públicas; docs/escopo-mvp.md sem decisões em aberto pendentes; docs/arquitetura.md e docs/mermaid.md coerentes com o código. (2) Dependências: conferir cada versão do requirements.txt com o PyPI, com a data da consulta; python -m pip check sem conflitos; se alguma versão mudar, ler as notas de versão, repetir os testes mínimos do roteiro e atualizar a tabela do CLAUDE.md e o README (Stack).
Estilo: Fato verificado separado de opinião; fontes e datas citadas; nenhuma versão atualizada sem justificativa.
Resposta: Relatório das divergências encontradas e corrigidas, tabela de versões conferidas e saída da definição de pronto.
```

### Prompt 40 - fechamento da v0.5.0

```text
Contexto: Revisões RT-11 a RT-14 concluídas na branch refactor/revisao-v050 com a definição de pronto verde.
Objetivo: Aplicar "Fechamento de release" do CLAUDE.md: README por inteiro (status, roadmap com a v0.5.0 concluída, Uso de IA generativa); docs/arquitetura.md com os ADRs promovidos; docs/backlog.md com RT-11 a RT-14 concluídos e horas reais; CHANGELOG.md com a seção 0.5.0; docs/HISTORY-IA.md com os Prompts 36 a 40 e a consolidação; CLAUDE.md corrigido no que a revisão mostrou divergente das fontes de verdade.
Estilo: README como o projeto está.
Resposta: Lista dos arquivos alterados. Git, após minha aprovação: commits, merge --no-ff em main, tag anotada v0.5.0 e push; definição de pronto em clone limpo.
```

## `v1.0.0`: entrega do curso (2 h no backlog)

### Prompt 41 - blueprint da v1.0.0

```text
Contexto: Release v1.0.0 (entrega) do backlog: RT-15 a RT-17; docs/requerimentos.md e a rastreabilidade da seção 7 de docs/escopo-mvp.md; horas reais acumuladas frente ao orçamento de cerca de 30 h.
Objetivo: Escrever docs/blueprint-v100.md: roteiro da validação em máquina limpa (diretório temporário fora do repositório, comandos do README em PowerShell e em Bash, resultado esperado de cada um); lista de verificação do histórico de uso de IA (prompts sem registro de execução, entradas faltantes no HISTORY-IA.md, modelos ausentes do README); checklist de publicação (rastreabilidade, status do README, CHANGELOG.md, tag, Release no GitHub); critério de parada se um requisito do curso não estiver atendido; estimativa frente às 2 h.
Estilo: Blueprint curto; sem decisões em aberto; sem código.
Resposta: Apenas docs/blueprint-v100.md, para aprovação. Git: branch docs/entrega-v100 a partir de main; adicionar; não comitar.
```

### Prompt 42 - validação em máquina limpa

```text
Contexto: docs/blueprint-v100.md aprovado. Item RT-15; RNF-01 e RNF-02; README (Como rodar) como única interface de operação.
Objetivo: Em um diretório temporário fora do repositório, clonar o repositório, criar o .venv, instalar, subir a API e rodar a definição de pronto usando só os comandos do README, em PowerShell; repetir em Git Bash ou registrar como não verificado; chamar /health e os exemplos de Endpoints; aplicar a Solução de problemas do README se o Smart App Control bloquear o SQLAlchemy; conferir que nenhum arquivo além de tasks.db e dos caches ignorados é criado.
Estilo: Roteiro passo a passo com o resultado de cada comando; falha reportada com a saída, nunca omitida.
Resposta: Relatório da validação, correções no README se algum comando falhar e remoção do clone de validação ao final.
```

### Prompt 43 - consolidação do histórico de uso de IA

```text
Contexto: Item RT-16; RNF-15; requisito R3.4 do curso; docs/PRE-HISTORY-IA.md, docs/EXTRA-HISTORY-IA.md, docs/HISTORY-IA.md, prompts/ e README (Uso de IA generativa).
Objetivo: Conferir que todo arquivo de prompts/ tem o registro da execução (modelo, data, resumo, interações seguintes); que docs/HISTORY-IA.md tem uma entrada por prompt, a consolidação de cada release e as observações transversais; escrever a análise final (ganho de produtividade acumulado, principais desafios, decisões que ficaram com o humano, lições); README listando todos os assistentes, modelos e etapas apoiadas por IA, com os links para os três históricos.
Estilo: Só fatos registrados nos arquivos; estimativas marcadas como estimativas; sem reconstruir conversas não registradas.
Resposta: Diffs de docs/HISTORY-IA.md e do README; lista das lacunas encontradas e de como foram tratadas.
```

### Prompt 44 - publicação da entrega

```text
Contexto: Item RT-17; validação e histórico concluídos na branch docs/entrega-v100; docs/requerimentos.md e a rastreabilidade da seção 7 de docs/escopo-mvp.md; CHANGELOG.md.
Objetivo: Fechar a release v1.0.0 conforme o CLAUDE.md: rastreabilidade toda como atendida; status do README como concluído e roadmap com todas as releases concluídas; CHANGELOG.md com a seção 1.0.0; docs/backlog.md fechado com horas reais e totais; docs/HISTORY-IA.md com os Prompts 41 a 44; após minha autorização, commits, merge --no-ff em main, tag anotada v1.0.0, push e Release no GitHub com o texto do CHANGELOG.md (gh release create); definição de pronto no clone final.
Estilo: Checklist de entrega com evidência (URL da tag e da Release); item não atendido reportado explicitamente, nunca omitido.
Resposta: Checklist concluída e URLs da tag e da Release.
```
