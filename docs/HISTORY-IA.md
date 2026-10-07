# Histórico do uso de IA generativa

Registro cronológico de como a IA generativa foi usada no desenvolvimento do projeto: em que fase do ciclo de vida, com que *prompt*, com que ganho e com que dificuldades. É a base do histórico de uso de IA exigido pelo curso e permite, ao final, uma leitura acadêmica do processo.

## Como ler este arquivo

- O uso de IA anterior ao repositório (concepção do `CLAUDE.md` no Claude em modo *chat*, em 01 e 02/10/2026) está em [`PRE-HISTORY-IA.md`](PRE-HISTORY-IA.md). Este arquivo começa no Prompt 00.
- Cada entrada corresponde a uma interação relevante e referencia o arquivo do *prompt* em [`prompts/`](../prompts/), onde estão o texto enviado e o registro da execução.
- Campos de cada entrada: data, fase do ciclo de vida, modelo/assistente, como a IA foi usada, *prompt* aplicado, refinamentos, ganho percebido e desafios.
- O **ganho percebido** é uma estimativa das horas que a mesma tarefa levaria sem IA, menos o tempo efetivamente gasto. É uma percepção, não uma medição, e deve ser lida como ordem de grandeza.
- Toda saída da IA foi revisada pelo autor antes de entrar na *branch* `main`. As decisões de escopo ficaram com o humano.

## Ambiente

| Item | Valor |
| --- | --- |
| Assistente | Claude Code (CLI), no VS Code, em Windows 11 com PowerShell |
| Modelo | Claude Opus 5.5 (`claude-opus-5-5`) por padrão, inclusive nos Prompts 21, 24, 25 e 31; outros modelos indicados na entrada (Fable 5.1 no Prompt 20, Sonnet 5.5 nos Prompts 22, 23 e 26 a 30) |
| Regras de trabalho com a IA | [`CLAUDE.md`](../CLAUDE.md) |
| Formato dos *prompts* | Contexto, Objetivo, Estilo, Resposta (e Observações, a partir do Prompt 04) |

## Resumo

| # | Data | Fase | Entrega | Ganho percebido |
| --- | --- | --- | --- | --- |
| 00 | 03/10/2026 | Planejamento / configuração | estrutura de diretórios, `git init`, primeiro *commit* | ~0,5 h |
| 01 | 03/10/2026 | Configuração | `.gitignore` revisado | ~0,5 h |
| 02 | 03/10/2026 | Documentação | `README.md` inicial, revisão contra os requisitos | ~1 h |
| 03 | 03/10/2026 | Configuração / dependências | `requirements.txt` com versões verificadas | ~1,5 h |
| 04 | 03/10/2026 | Arquitetura | `docs/arquitetura.md` (Mermaid e ADRs), roadmap | ~2,5 h |
| 05 | 03/10/2026 | Documentação / licenciamento | `LICENSE` (MIT) | ~0,2 h |
| 06 | 03/10/2026 | Documentação do processo | este arquivo | ~1 h |
| 07 | 03/10/2026 | Publicação / verificação | *push* para o GitHub, conferência do clone e dos diagramas Mermaid | ~0,5 h |
| 08 | 04/10/2026 | Revisão / publicação de *release* | revisão da `v0.1.0`, checagem de APIs deprecadas, correção do `.venv`, `CHANGELOG.md`, *tag* `v0.1.0` | ~3 h |
| 10 | 04/10/2026 | Requisitos / escopo | `docs/escopo-mvp.md` (requisitos funcionais e não funcionais, fora de escopo, decisões em aberto) | ~1,5 h |
| 11 | 04/10/2026 | Planejamento / backlog | `docs/backlog.md` (itens RF/RT por *release*, critérios de aceite, estimativas) | ~1,5 h |
| 12 | 04/10/2026 | Arquitetura / revisão | revisão dos diagramas Mermaid, ADR-12, `docs/mermaid.md` (antes e depois), *merge* e *push* | ~2 h |
| 13 | 04/10/2026 | Processo / revisão humana | `docs/PRE-HISTORY-IA.md`, regras de código e de *blueprint* executável no `CLAUDE.md`, renomeação do Prompt 00 | ~0,7 h |
| 20 | 05/10/2026 | Planejamento do desenvolvimento | `prompts/prompts-desenvolvimento.md` (Prompts 21 a 44) | ~1,5 h |
| 21 | 05/10/2026 | Planejamento / *blueprint* | `docs/blueprint-v020.md`, com protótipo verificado fora do repositório | ~2 h |
| 22 | 05/10/2026 | Código / testes | `settings.py`, `base.py`, `database.py`, DT-02 e DT-03, 8 testes | ~1 h |
| 23 | 05/10/2026 | Código / testes / execução | `/health` em camadas, `main.py`, 13 testes, ADR-13, DT-01, execução manual | ~1,5 h |
| 24 | 05/10/2026 | Documentação / fechamento de *release* | README, diagramas, backlog, `CHANGELOG.md`, este histórico, `CLAUDE.md` | ~1,5 h |
| 25 | 05/10/2026 | Planejamento / *blueprint* | `docs/blueprint-v030.md`, com protótipo verificado e rodada do roteiro de APIs | ~2,5 h |
| 26 | 05/10/2026 | Código / testes | `UTCDateTime`, esquemas e modelo `Task`, DT-04 e DT-05, 2 testes | ~1 h |
| 27 | 05/10/2026 | Código / testes | `TaskRepository`, 2 testes | ~0,5 h |
| 28 | 05/10/2026 | Código / testes | `TaskService`, ADR-14, DT-06 e DT-07, 14 testes unitários | ~1 h |
| 29 | 05/10/2026 | Código / testes | rotas de `/tasks`, tradutores de erro, ADR-15, DT-08, 38 casos de integração | ~2 h |
| 30 | 06/10/2026 | Documentação / execução | seção Endpoints do README, com exemplos executados na API | ~1 h |
| 31 | 06/10/2026 | Documentação / fechamento de *release* | README, diagramas, escopo, backlog, `CHANGELOG.md`, este histórico, `CLAUDE.md` | ~1,5 h |
| 32 | 06/10/2026 | Planejamento / *blueprint* | `docs/blueprint-v040.md`, com protótipo verificado e revisão das datas no horário local (D-09) | ~3 h |
| 33 | 06/10/2026 | Código / testes | `priority_advisor` (funções puras), DT-09, 22 testes unitários | ~1 h |
| 34 | 06/10/2026 | Código / testes / documentação | integração do *advisor* ao *service* e às rotas, filtro por prioridade, datas no horário local, DT-10 a DT-15, ADR-16 a ADR-18, exemplos do README, 43 testes | ~3,5 h |
| 35 | 06/10/2026 | Documentação / fechamento de *release* | README, diagramas, escopo, backlog, `CHANGELOG.md`, este histórico | ~1,5 h |
| 36 | 06/10/2026 | Planejamento / *blueprint* | `docs/blueprint-v050.md` (revisão), com levantamento prévio no código | ~1 h |
| 37 | 06/10/2026 | Revisão de arquitetura | checklist de 16 verificações, ADR-19 e ADR-20, sem desvio de código | ~1 h |
| 38 | 07/10/2026 | Revisão de segurança | checklist de 17 verificações, `TaskId` (DT-16), `hide_parameters` (DT-17), 9 casos de teste, retirada do mypy (ADR-21) | ~1 h |
| 39 | 07/10/2026 | Revisão de documentação e dependências | versões conferidas no PyPI e na OSV, sem mudança; exemplos do README executados de novo; checklist de 21 verificações | ~1 h |
| 40 | 07/10/2026 | Documentação / fechamento de *release* | README, `CLAUDE.md`, escopo, backlog, `CHANGELOG.md`, este histórico | ~1,5 h |

## Entradas

### Prompt 00: estrutura e repositório

- **Data:** 03/10/2026
- **Fase:** planejamento e configuração do ambiente
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:** geração da estrutura de diretórios a partir do `CLAUDE.md`, criação do `.gitignore` inicial, `git init` em `main` e primeiro *commit*
- **Prompt:** [`prompts/Prompt 00 - criar diretorios e main`](../prompts/Prompt%2000%20-%20criar%20diretorios%20e%20main) (nome original `Prompt00 - Inicio`, renomeado no Prompt 13)
- **Refinamentos:** nenhum
- **Ganho percebido:** ~0,5 h
- **Desafios:**
  - O pedido "estrutura sem arquivos" conflita com o fato de o git não versionar diretórios vazios. A IA não usou `.gitkeep`, porque o `CLAUDE.md` proíbe arquivos criados por antecipação, e informou que os diretórios entram no repositório com seus primeiros arquivos.
  - O nome pedido para o *prompt* diferia do exemplo do `CLAUDE.md`; prevaleceu o pedido do usuário.
  - O `.gitignore` gerado nesta etapa continha um erro (`.env.*` também ignorava o `.env.example`), corrigido pela própria IA no Prompt 01.

### Prompt 01: `.gitignore`

- **Data:** 03/10/2026
- **Fase:** configuração do ambiente
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:** revisão e correção do `.gitignore`, organizado por tecnologia; verificação com `git check-ignore` sobre caminhos de exemplo
- **Prompt:** [`prompts/Prompt 01 - criar .gitignore`](../prompts/Prompt%2001%20-%20criar%20.gitignore)
- **Refinamentos:** nenhum
- **Ganho percebido:** ~0,5 h
- **Desafios:**
  - O *prompt* pedia padrões de Node.js para um *frontend* que está fora do MVP, e o `CLAUDE.md` proíbe antecipar configuração para itens futuros. A IA atendeu ao pedido explícito e registrou a divergência.
  - A verificação por comando (`git check-ignore`), e não só a leitura do arquivo, confirmou que `app/`, `tests/` e `.env.example` continuavam versionáveis.

### Prompt 02: `README.md`

- **Data:** 03/10/2026
- **Fase:** documentação
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:** redação do README inicial (objetivo, escopo, prioridades, *stack*, como rodar, roadmap, uso de IA, limitações, licença); revisão posterior contra `docs/requerimentos.md`
- **Prompt:** [`prompts/Prompt 02 - criar o README`](../prompts/Prompt%2002%20-%20criar%20o%20README)
- **Refinamentos:** após o usuário adicionar `docs/requerimentos.md`, o README ganhou a seção "Créditos e licença" e a menção à *tag* `v1.0.0`
- **Ganho percebido:** ~1 h
- **Desafios:**
  - Na primeira tentativa, o arquivo do *prompt* estava vazio no disco (não salvo no editor); a IA identificou e pediu para salvar, em vez de supor o conteúdo.
  - O *prompt* citava `docs/requerimentos.md`, que ainda não existia; a IA usou o `CLAUDE.md` como fonte e revisou o README quando o arquivo chegou.
  - O contexto do *prompt* dizia "priorização assistida por IA" no MVP, em conflito com o `CLAUDE.md`. A IA seguiu o `CLAUDE.md` e pediu decisão; o usuário confirmou depois que esse item fica fora do MVP.
  - O roadmap foi proposto pela IA, sem fonte anterior, e marcado como proposta para validação humana.

### Prompt 03: `requirements.txt`

- **Data:** 03/10/2026
- **Fase:** configuração e gestão de dependências
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:** consulta das versões atuais no PyPI, instalação em ambiente virtual, verificação de compatibilidade (`pip check`, `Requires-Python`, marcadores de plataforma), geração do `requirements.txt` em UTF-8 sem BOM, atualização do README (Stack, Configuração), três *commits* e *merge* em `main`
- **Prompt:** [`prompts/Prompt 03 - criar requirements.txt atualizado`](../prompts/Prompt%2003%20-%20criar%20requirements.txt%20atualizado)
- **Refinamentos:** o usuário pediu para recuperar o *prompt* original e substituir o registro da execução por um resumo
- **Ganho percebido:** ~1,5 h
- **Desafios:**
  - **Conhecimento do modelo versus realidade instalada:** o Starlette 1.7.0 passou a exigir `httpx2` no `TestClient`, e o `httpx` emite aviso de deprecação. Esse achado só apareceu ao executar código no ambiente real; um assistente que gerasse o arquivo de memória teria fixado `httpx`, e os testes falhariam com `-W error`. O caso confirma a regra do `CLAUDE.md` de verificar versões por execução e registrar fonte e data.
  - O *merge* foi abortado porque o `README.md` estava aberto no LibreOffice e o Windows impediu o git de removê-lo. A IA conferiu por *hash* que nada havia se perdido e concluiu o *merge* depois que o arquivo foi fechado.
  - A IA fez três *commits* em vez de um, separados por assunto, o que diverge do pedido e foi informado; a motivação é o histórico de *commits* exigido pelo curso.

### Prompt 04: arquitetura

- **Data:** 03/10/2026
- **Fase:** arquitetura e projeto
- **Modelo:** Claude Opus 5.5, via Claude Code; o próprio *prompt* foi redigido com auxílio do mesmo modelo
- **Uso da IA:** *blueprint* com riscos e decisões em aberto, aprovado antes da escrita; criação de `docs/arquitetura.md` com diagramas Mermaid (módulos e dependências, fluxo de dados, modelo de dados) e dez ADRs; reformulação do roadmap em seis *releases*; ajustes no README e no `CLAUDE.md`
- **Prompt:** [`prompts/Prompt 04 - desenho de arquitetura minimo`](../prompts/Prompt%2004%20-%20desenho%20de%20arquitetura%20minimo)
- **Refinamentos:** aprovação do *blueprint* com quatro decisões do usuário (roadmap, peças do `/health`, registro do 404, organização das *branches*)
- **Ganho percebido:** ~2,5 h
- **Desafios:**
  - O *prompt* supunha um roadmap (v0.2.0 a v0.5.0) que não existia no README; a IA expôs a divergência no *blueprint*, e o roadmap foi refeito por decisão do usuário.
  - O *prompt* pedia o código 404 em fluxos que não o retornam (`POST /tasks` e `/health`); a solução aprovada foi uma nota no fluxo de dados.
  - Erro de digitação na aprovação ("444"), interpretado como 404 e registrado.
  - Os diagramas não puderam ser renderizados localmente (sem Node.js na máquina); a sintaxe foi revisada manualmente e depende de confirmação no GitHub.
  - A IA acrescentou um ADR não previsto (datas em UTC, já que o SQLite não guarda fuso horário), antecipando um risco de implementação.

### Prompt 05: licença

- **Data:** 03/10/2026
- **Fase:** documentação e licenciamento
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:** criação do `LICENSE` com o texto oficial da licença MIT; inclusão do arquivo na estrutura do `CLAUDE.md` e no README
- **Prompt:** [`prompts/Prompt 05 - criar a licenca mit`](../prompts/Prompt%2005%20-%20criar%20a%20licenca%20mit)
- **Refinamentos:** nenhum
- **Ganho percebido:** ~0,2 h
- **Desafios:**
  - O *prompt* pedia Markdown; a IA manteve texto puro e o texto oficial em inglês, sem alterações, para que o GitHub reconheça a licença.

### Prompt 06: histórico de uso de IA

- **Data:** 03/10/2026
- **Fase:** documentação do processo
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:** consolidação deste histórico a partir dos arquivos de `prompts/`, do histórico do git e da conversa; separação das mudanças pendentes em *commits* por assunto, *merge* em `main` e limpeza de *branches*
- **Prompt:** [`prompts/Prompt 06 - criar o HISTORY-IA.md`](../prompts/Prompt%2006%20-%20criar%20o%20HISTORY-IA.md)
- **Refinamentos:** nenhum
- **Ganho percebido:** ~1 h
- **Desafios:**
  - As estimativas de ganho foram feitas pela IA e dependem de validação do autor.

### Prompt 07: publicação no GitHub

- **Data:** 03/10/2026
- **Fase:** publicação e verificação
- **Modelo:** Claude Opus 5.5, via Claude Code, com a extensão Claude in Chrome para inspecionar a página
- **Uso da IA:** varredura de segredos antes da publicação, *push* de `main`, comparação de um clone limpo com o repositório local, verificação da licença pela API do GitHub e conferência visual da renderização dos 5 diagramas Mermaid no navegador
- **Prompt:** [`prompts/Prompt 07 - push GitHub visualizacao mermaid`](../prompts/Prompt%2007%20-%20push%20GitHub%20visualizacao%20mermaid)
- **Refinamentos:** nenhum
- **Ganho percebido:** ~0,5 h
- **Desafios:**
  - A renderização Mermaid do GitHub acontece no navegador, então não basta conferir o arquivo publicado; foi preciso abrir a página e inspecionar cada diagrama. Isso fechou a pendência do Prompt 04, que não pôde renderizar localmente.
  - A captura de tela da página travou algumas vezes; capturas isoladas resolveram.
  - Diretórios vazios (`app/`, `tests/`) não aparecem no GitHub, como já previsto no Prompt 00.

### Prompt 08: revisão de publicação da release v0.1.0

- **Data:** 04/10/2026
- **Fase:** revisão e publicação de *release*
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:**
  - revisão crítica em formato de checklist, com severidade "bloqueia" e "recomenda": *commits*, APIs deprecadas, ambiente virtual, `.gitignore` e requisitos do curso;
  - testes mínimos dos 8 padrões do roteiro de checagem, num diretório temporário;
  - diagnóstico e correção do `.venv`;
  - criação do `CHANGELOG.md`;
  - fechamento da *release*: README, `CLAUDE.md`, ADR-11, *merge*, *tag* `v0.1.0` e *push*;
  - relatório em [`docs/release-review-010.md`](release-review-010.md).
- **Prompt:** [`prompts/Prompt 08 - revisao critica release 010`](../prompts/Prompt%2008%20-%20revisao%20critica%20release%20010)
- **Refinamentos:** nenhum. O autor aprovou todos os itens propostos de uma vez e autorizou o *push* e a *tag*.
- **Ganho percebido:** ~3 h
- **Desafios:**
  - **Smart App Control.** O Windows bloqueava as extensões compiladas do SQLAlchemy, e `import sqlalchemy` falhava. O defeito passou despercebido no Prompt 03 porque o `pip check` valida metadados, não importações. Ele só apareceu ao executar código real. A correção (reinstalar a mesma versão em Python puro) foi testada num ambiente virtual descartável antes de tocar o `.venv`.
  - **Comando do mypy.** O comando da definição de pronto (`mypy app`) falharia na estrutura decidida na ADR-03. A simulação da estrutura revelou isso antes de existir código e gerou a ADR-11.
  - **`declarative_base()`.** Não emite aviso no SQLAlchemy 2.1.3, então o critério "emite aviso" não o pega. Foi classificado como estilo legado.
  - **Histórico publicado.** Reescrever o histórico exigiria *force push*. A decisão humana foi corrigir a descrição do `94f30f2` só no CHANGELOG e registrar regras para os *merges* futuros.
  - **Release no GitHub.** O `gh` não está instalado, então a Release ficou como passo manual. A *tag* foi publicada.
  - **Definição de pronto.** Numa *release* sem código, ela não se aplica. Foi registrada como "não aplicável", e não como aprovada, para não mascarar o estado do projeto.

### Prompt 10: escopo e não escopo do MVP

- **Data:** 04/10/2026
- **Fase:** engenharia de requisitos (entre a `v0.1.0` e a `v0.2.0`)
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:**
  - consolidação, em [`docs/escopo-mvp.md`](escopo-mvp.md), do escopo espalhado pelo README, pelo `CLAUDE.md` e por `docs/arquitetura.md`;
  - redação de 13 requisitos funcionais com critério de aceitação e *release* prevista, e de 15 não funcionais com forma de verificação;
  - separação do fora de escopo em previsões futuras (com motivo) e itens excluídos sem previsão;
  - tabela de decisões em aberto com recomendação, e rastreabilidade com `docs/requerimentos.md`;
  - atualização do README, do `CLAUDE.md` (fonte de verdade, Ponto de partida, estrutura), de `docs/arquitetura.md` e do `CHANGELOG.md`; *branch* `docs/escopo-mvp`, sem *commit*, como pedido.
- **Prompt:** [`prompts/Prompt 10 - criacao do escopo e nao escopo`](../prompts/Prompt%2010%20-%20criacao%20do%20escopo%20e%20nao%20escopo)
- **Refinamentos:** nenhum
- **Ganho percebido:** ~1,5 h
- **Desafios:**
  - **Fonte de verdade duplicada.** O `CLAUDE.md` definia o README como dono do escopo. Um segundo documento de escopo criaria duas fontes. A IA tornou `docs/escopo-mvp.md` o dono dos requisitos e deixou no README o resumo e os links.
  - **Estrutura fechada.** O arquivo novo não constava da estrutura do `CLAUDE.md`. Como a estrutura permite ajustar arquivos dentro de `docs/`, ele foi acrescentado a ela.
  - **Não decidir pelo autor.** Prioridade padrão, valores de *status*, coerência entre prioridade 4 e data/hora e regras do `priority_advisor` continuam em aberto, com recomendação. A IA acrescentou duas decisões que o desenho anterior não explicitava: a rota da marcação como concluída e o momento de criar a coluna `priority` (sem migrações, criá-la só na `v0.4.0` alteraria o esquema).
  - **Fora de escopo sem ampliar escopo.** A lista de itens excluídos sem previsão (por exemplo, *deploy*, notificações, busca textual) só delimita o MVP; nenhum deles virou meta.
  - **Numeração.** Não existe Prompt 09 em `prompts/`; a numeração segue o nome dado pelo autor.

### Prompt 11: backlog por release

- **Data:** 04/10/2026
- **Fase:** planejamento
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:**
  - desdobramento dos requisitos de `docs/escopo-mvp.md` em [`docs/backlog.md`](backlog.md), organizado pelas *releases* `v0.2.0` a `v1.0.0`;
  - 13 itens RF (mesmos IDs do escopo) e 17 itens RT, cada um com critérios de aceite marcados por forma de verificação (teste, inspeção ou comando), RNF atendidos, estimativa e situação;
  - critérios comuns a todos os itens e ao fechamento de *release*, para não repetir a definição de pronto em cada linha;
  - tabela de rastreabilidade RNF → itens;
  - atualização do `CLAUDE.md` (fonte de verdade, estrutura, fechamento de *release*), do README, do escopo e do `CHANGELOG.md`.
- **Prompt:** [`prompts/Prompt 11 - criar o backlog por release`](../prompts/Prompt%2011%20-%20criar%20o%20backlog%20por%20release)
- **Refinamentos:** nenhum
- **Ganho percebido:** ~1,5 h
- **Desafios:**
  - **Significado de "RT".** O *prompt* não define a sigla, e o escopo usa RNF. A IA interpretou RT como requisito técnico (infraestrutura, código interno, testes, documentação, publicação), ligado aos RNF que atende, e manteve os IDs RF do escopo para haver uma única numeração.
  - **Itens que dependem de decisões em aberto.** RF-07, RF-10 e RF-11 têm critérios condicionados às decisões D-02, D-05 e D-07; o filtro por prioridade (D-06) ficou como item condicionado, sem ID ativo, para não ampliar o escopo.
  - **Orçamento.** A soma das estimativas (18,5 h) foi conferida e corrigida durante a execução; o tempo real gasto na `v0.1.0` não foi medido, então a folga frente às 30 h é uma estimativa.
  - **Mudanças do Prompt 10 sem *commit*.** A *branch* `docs/backlog` foi criada com as mudanças do Prompt 10 ainda no *stage*, porque o backlog depende do escopo; os dois conjuntos ficaram no mesmo *stage*.

### Prompt 12: revisão dos diagramas Mermaid

- **Data:** 04/10/2026
- **Fase:** arquitetura (revisão do desenho antes do código)
- **Modelo:** Claude Opus 5.5, via Claude Code; Claude in Chrome para conferir a renderização no GitHub
- **Uso da IA:**
  - análise dos 5 diagramas (1 no README e 4 em `docs/arquitetura.md`) contra o `CLAUDE.md`, os ADRs, o escopo e o backlog;
  - relatório enumerado para aprovação, separando alterações necessárias, recomendadas e não recomendadas;
  - execução do aprovado: aresta `task_service → task`, `commit` e `refresh` no fluxo de `POST /tasks` (nova ADR-12), padrões em aberto no modelo de dados, diagramas novos de erros em `/tasks/{id}` e de testes;
  - criação de [`docs/mermaid.md`](mermaid.md) com o antes e o depois de cada diagrama, com destaque visual das mudanças (`linkStyle` e `rect`), gerado a partir do *commit* anterior para garantir cópias fiéis;
  - *commits*, *merge* em `main` e *push*.
- **Prompt:** [`prompts/Prompt 12 - atualizacao do mermaid`](../prompts/Prompt%2012%20-%20atualizacao%20do%20mermaid)
- **Refinamentos:** o autor aprovou os itens com duas ressalvas. O esquema da resposta de `/health` ficou para o *blueprint* da `v0.2.0` (registrado como D-08). O `docs/mermaid.md` passou a ter o antes e o depois, de forma didática, em vez de só os diagramas atualizados.
- **Ganho percebido:** ~2 h
- **Desafios:**
  - **Revisar diagrama é revisar desenho.** As duas inconsistências reais eram lacunas de projeto, não erros de sintaxe: uma dependência escondida entre camadas e a ausência de responsável pelo `commit`. A segunda virou ADR antes de existir código.
  - **Não decidir pelo autor.** A IA propôs `health_schemas.py`, mas ofereceu deixar a escolha para o *blueprint*; o autor escolheu adiar.
  - **Cópias de diagramas.** Um catálogo separado pode divergir da versão oficial. Mitigação: `docs/arquitetura.md` continua dono, e o `CLAUDE.md` passou a exigir a atualização dos dois lugares.
  - **Limites do Mermaid.** O `erDiagram` não permite destacar um atributo com cor; a mudança foi explicada em texto.
  - **Renderização.** Sem Node.js na máquina, a validação da sintaxe depende do GitHub: a *branch* foi publicada antes do *merge* e conferida no navegador. Os 10 diagramas do catálogo e os 6 de `docs/arquitetura.md` renderizaram, com os destaques visíveis. A captura de tela travou duas vezes, como no Prompt 07; a navegação direta por âncora resolveu.

### Prompt 13: correções a partir da revisão humana

- **Data:** 04/10/2026
- **Fase:** processo e governança do uso de IA
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:**
  - renomeação de `Prompt00 - Inicio` para `Prompt 00 - criar diretorios e main` (`git mv`, preservando o histórico) e atualização das referências;
  - criação de [`PRE-HISTORY-IA.md`](PRE-HISTORY-IA.md) a partir da declaração do autor sobre as sessões de 01 e 02/10/2026 no Claude em modo *chat*;
  - regras no `CLAUDE.md`: nomenclatura semântica, funções coesas, tipagem e registro de decisões técnicas (DT) em `docs/decisoes.md`, com o limite entre DT e ADR;
  - regra de *blueprint* executável, para que o Claude Sonnet 5.5 possa segui-lo sem erro: arquivo próprio por *release*, sem decisões em aberto, passos com assinaturas tipadas, testes nomeados, comando de verificação e condição de parada;
  - atualização do README (Uso de IA generativa), do `CHANGELOG.md` e deste arquivo.
- **Prompt:** [`prompts/Prompt 13 - correcoes e revisao humana`](../prompts/Prompt%2013%20-%20correcoes%20e%20revisao%20humana)
- **Refinamentos:** nenhum
- **Ganho percebido:** ~0,7 h
- **Desafios:**
  - **Registrar sem inventar.** A pré-história se apoia só na declaração do autor; a IA não reconstruiu o conteúdo das conversas e marcou a fonte no próprio arquivo. A única informação acrescentada (as seções do `CLAUDE.md` inicial) foi conferida no *commit* `94f30f2`.
  - **Duas casas para decisões.** O `CLAUDE.md` já mandava registrar decisões nos ADRs. A IA definiu o limite: decisão estrutural é ADR; decisão local ao código é DT.
  - **Onde guardar o *blueprint*.** Para outro modelo segui-lo, o *blueprint* precisa existir fora do *chat*. A IA definiu o arquivo `docs/blueprint-vXYZ.md`, no padrão de `docs/release-review-010.md`.
  - **Arquivo por antecipação.** O `docs/decisoes.md` não foi criado vazio, por regra do `CLAUDE.md`; nasce com a primeira DT.
  - **Referências históricas.** O `docs/release-review-010.md` cita o nome antigo do Prompt 00; foi mantido, por ser um relatório datado.

### Prompt 20: prompts para a fase de desenvolvimento

- **Data:** 05/10/2026
- **Fase:** planejamento do desenvolvimento (`v0.2.0` a `v1.0.0`)
- **Modelo:** Claude Fable 5.1, via Claude Code. Antes, Claude Sonnet 5.5 em modo *chat* extraiu das capturas de tela do curso os *prompts* de exemplo do tutor, gravados em [`release-prompts-solon-020.md`](release-prompts-solon-020.md) (registro em [`EXTRA-HISTORY-IA.md`](EXTRA-HISTORY-IA.md))
- **Uso da IA:**
  - leitura do exemplo do tutor (seis *prompts* de "definições mínimas": modelos, *repository*, *service*, `PriorityAdvisor`, rotas e revisão) e das fontes de verdade do projeto (backlog, escopo, arquitetura, `CLAUDE.md`);
  - geração de [`prompts/prompts-desenvolvimento.md`](../prompts/prompts-desenvolvimento.md): 24 *prompts* (21 a 44) em sequência, por *release*, cada um com Contexto, Objetivo, Estilo e Resposta, citando os itens do backlog (RT/RF), as decisões (D-NN) e os ADRs que cobre;
  - adaptação do exemplo ao processo do projeto: um *prompt* de *blueprint* por *release* (com as decisões tomadas no texto, a confirmar na aprovação), *prompts* de execução por item do backlog e um *prompt* de fechamento; a "revisão técnica" do tutor vira a *release* `v0.5.0`;
  - registro dos arquivos criados fora da estrutura original (`docs/EXTRA-HISTORY-IA.md`, `docs/release-prompts-solon-020.md`, `prompts/prompts-desenvolvimento.md`) no `CLAUDE.md` e no README.
- **Prompt:** [`prompts/Prompt 20 - criando os prompts para desenvolvimento`](../prompts/Prompt%2020%20-%20criando%20os%20prompts%20para%20desenvolvimento)
- **Refinamentos:** nenhum até a revisão do autor; o arquivo foi entregue como proposta.
- **Ganho percebido:** ~1,5 h (estimativa: mapear 30 itens do backlog, 8 decisões e 12 ADRs em *prompts* coerentes com o `CLAUDE.md`)
- **Desafios:**
  - **Exemplo com premissas diferentes.** O tutor usa *repository* em memória, `PriorityAdvisor` com LLM opcional via `OPENAI_API_KEY` e um arquivo de código por *prompt*. O projeto decidiu SQLite com SQLAlchemy, `priority_advisor` determinístico (escopo, seção 5.1) e *blueprint* aprovado antes do código. A IA manteve o formato dos campos e trocou o conteúdo, sem reabrir decisões.
  - **Passos ainda não existem.** Os *prompts* de execução não podem citar números de passo, porque cada *blueprint* será escrito depois; citam os itens RT/RF e deixam ao *blueprint* a ordem exata.
  - **Decisões D-NN.** O `CLAUDE.md` exige *blueprint* sem decisões em aberto, mas a decisão é do autor. Os *prompts* de *blueprint* mandam tomar a decisão no texto com a recomendação do escopo, para confirmação na aprovação.
  - **Campo TOM.** Os *prompts* deste projeto usam cinco campos (com TOM); o exemplo do tutor, quatro. Seguiu-se o exemplo, como pedido.
  - **Estado do git.** A *branch* anterior (`docs/correcoes-revisao-humana`) tinha alterações no *stage* sem *commit*; a nova *branch* foi criada do mesmo ponto e carrega essas alterações. Separá-las em *commits* distintos fica para o autor.

## Release v0.1.0: consolidação

- **Período:** 03/10/2026 a 04/10/2026 (Prompts 00 a 08)
- **Entregas:**
  - `.gitignore`, `CLAUDE.md`, README e `docs/requerimentos.md`;
  - `requirements.txt` verificado;
  - `docs/arquitetura.md` (4 diagramas Mermaid, mais 1 no README, e 11 ADRs);
  - `LICENSE`, este histórico, `CHANGELOG.md` e `docs/release-review-010.md`;
  - publicação no GitHub com *tag* `v0.1.0`.
- **Uso da IA:** geração de documentação, verificação de versões no PyPI, desenho da arquitetura, revisão contra requisitos, testes de APIs deprecadas e diagnóstico de ambiente. Nenhum código da aplicação foi gerado nesta *release*.
- **Ganho percebido acumulado:** ~10,7 h (soma das estimativas dos Prompts 00 a 08).
- **Lição principal:** a verificação por execução encontrou dois defeitos que a leitura de documentação não revelaria:
  - o `httpx2` (Prompt 03);
  - o bloqueio do SQLAlchemy pelo Smart App Control e o comando do mypy (Prompt 08).

  Na `v0.2.0`, o primeiro código já nasce sob o roteiro de checagem preenchido.

## Entradas da release v0.2.0

### Prompt 21: *blueprint* da `v0.2.0`

- **Data:** 05/10/2026
- **Fase:** planejamento da *release* `v0.2.0`
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code. O arquivo do *prompt* não tinha o registro; o modelo foi identificado no Prompt 24 pelo transcrito local da sessão que gravou o *blueprint*
- **Uso da IA:**
  - leitura do backlog (RT-01 a RT-04, RF-12, RF-13), do escopo (D-08), dos ADRs e do roteiro de checagem de APIs;
  - geração de [`docs/blueprint-v020.md`](blueprint-v020.md) no formato de *blueprint* executável do `CLAUDE.md`: decisões tomadas (D-08, DT-01 a DT-03), importações permitidas por arquivo, padrões proibidos, seis passos com assinaturas, testes nomeados e IDs, riscos, lista do que não fazer e estimativa;
  - verificação prévia: os trechos de código foram executados em protótipo fora do repositório, no `.venv` do projeto (13 testes com `-W error`, mypy sem erros, uvicorn respondendo).
- **Prompt:** [`prompts/Prompt 21 - blueprint da v0.2.0`](../prompts/Prompt%2021%20-%20blueprint%20da%20v0.2.0)
- **Refinamentos:** aprovado pelo autor sem alteração registrada.
- **Ganho percebido:** ~2 h (desenho detalhado e verificado de seis itens e três decisões técnicas)
- **Desafios:**
  - **Fábrica da aplicação.** Sem `create_app`, os testes criariam `tasks.db` na raiz pelo `lifespan` e não haveria como testar `production` sem recarregar módulos. O problema apareceu no protótipo e gerou a DT-01.
  - **Sintaxe do Python 3.12.** O *blueprint* proíbe `type X = ...`, porque o mínimo do projeto é 3.11, embora o ambiente rode 3.14.6.

### Prompt 22: configuração e acesso ao banco

- **Data:** 05/10/2026
- **Fase:** código e testes (`v0.2.0`, passos 1 e 2 do *blueprint*)
- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), via Claude Code, como modelo de execução que não participou do desenho
- **Uso da IA:** geração dos `__init__.py`, de `settings.py`, `base.py` e `database.py`, das DT-02 e DT-03 em [`docs/decisoes.md`](decisoes.md) e dos 8 primeiros testes, com a definição de pronto ao fim de cada passo.
- **Prompt:** [`prompts/Prompt 22 - configuração e acesso ao banco`](../prompts/Prompt%2022%20-%20configura%C3%A7%C3%A3o%20e%20acesso%20ao%20banco)
- **Refinamentos:** nenhum; sem divergência do *blueprint*.
- **Ganho percebido:** ~1 h
- **Desafios:** um comando de *shell* travou por um `python -` sem entrada, incluído por engano pelo assistente; os arquivos já estavam gravados e foram conferidos.

### Prompt 23: aplicação, `/health` e testes de integração

- **Data:** 05/10/2026
- **Fase:** código, testes e execução manual (`v0.2.0`, passos 3 a 5 do *blueprint*)
- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), via Claude Code
- **Uso da IA:**
  - geração de `health_schemas.py`, `health_service.py`, `health_routes.py`, `main.py` e dos 5 testes de integração restantes;
  - ADR-13 em `docs/arquitetura.md`, D-08 marcada como decidida e DT-01;
  - execução manual com `python -m uvicorn app.main:app --reload`: `/health` com `200` e corpo `ok`, `/docs` com `200`.
- **Prompt:** [`prompts/Prompt 23 - aplicação, health e testes de integração`](../prompts/Prompt%2023%20-%20aplica%C3%A7%C3%A3o%2C%20health%20e%20testes%20de%20integra%C3%A7%C3%A3o)
- **Refinamentos:** duas execuções interrompidas por erro de API. Na terceira, a IA verificou o estado antes de agir, encontrou o código e os testes gravados e completou só a documentação e a execução manual.
- **Ganho percebido:** ~1,5 h
- **Desafios:**
  - **Interrupções da API.** Retomar sem refazer exigiu conferir arquivo a arquivo contra o *blueprint*; o *blueprint* persistido em disco tornou isso possível sem depender do histórico do *chat*.
  - **Porta ocupada e arquivo preso.** A porta 8000 estava ocupada por um servidor do autor, que também mantinha o `tasks.db` aberto; a execução manual usou a porta 8765, e a IA não encerrou o processo que não iniciou.

### Prompt 24: fechamento da `v0.2.0`

- **Data:** 05/10/2026
- **Fase:** documentação e fechamento de *release*
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - revisão do README por inteiro (status, nova seção Endpoints com `GET /health`, Configuração, Como rodar, roadmap, Uso de IA generativa);
  - ajuste dos diagramas de módulos e de `/health` em `docs/arquitetura.md` e registro do antes e do depois em `docs/mermaid.md`;
  - backlog com os seis itens concluídos, `CHANGELOG.md` com a seção `0.2.0`, este histórico, remoção da seção Ponto de partida do `CLAUDE.md` e status do *blueprint*;
  - após aprovação do autor: *commits*, *merge*, *tag* `v0.2.0`, *push* e definição de pronto em clone limpo.
- **Prompt:** [`prompts/Prompt 24 - fechamento da v0.2.0`](../prompts/Prompt%2024%20-%20fechamento%20da%20v0.2.0)
- **Refinamentos:** duas interrupções por erro de API durante a execução; retomada a partir do estado em disco, sem perda.
- **Ganho percebido:** ~1,5 h
- **Desafios:**
  - **Horas reais.** O *prompt* pede as horas reais no backlog, mas elas não foram medidas; a IA não inventou números e o autor decidiu preenchê-las manualmente.
  - **Modelo do Prompt 21 sem registro.** Identificado pelo transcrito local da sessão (Claude Opus 5.5), em vez de suposto.
  - **Conferência dos diagramas.** Sem o Claude in Chrome conectado e sem Node.js na máquina, a sintaxe dos diagramas alterados foi validada pelo serviço mermaid.ink, com um diagrama quebrado como controle negativo.
- **Resultado do git:** *commits* `ce736f9`, `d2b66e9` e `9300575`; *merge* `e967174` em `main`; *tag* `v0.2.0` e *push* de `main`, da *tag* e da *branch*. Definição de pronto verde em clone limpo da *tag* (13 testes, mypy sem erros, `git status` limpo).
  - **Seção `[Não publicado]` do `CHANGELOG.md`.** As mudanças de documentação feitas em `main` depois da `v0.1.0` entram na `0.2.0`, porque a *tag* as inclui.

## Release v0.2.0: consolidação

- **Período:** 05/10/2026 (Prompts 21 a 24)
- **Entregas:** primeiro código da aplicação. São 11 arquivos em `app/`: configuração, banco, `/health` em camadas e composição com `create_app`. Somam-se 13 testes de integração em `tests/test_task_routes.py`, o *blueprint* executável, três DTs, o ADR-13, o README com a seção Endpoints e a *tag* `v0.2.0`.
- **Uso da IA:**
  - divisão de papéis entre modelos: o Opus 5.5 desenhou (Prompt 21) e fechou (Prompt 24) a *release*, e o Sonnet 5.5 executou o *blueprint* (Prompts 22 e 23) sem participar do desenho;
  - a execução seguiu o *blueprint* sem divergência de código, o que valida a regra de *blueprint* executável do `CLAUDE.md`.
- **Ganho percebido acumulado:** ~6 h (soma das estimativas dos Prompts 21 a 24).
- **Horas reais:** 4 h, informadas pelo autor em 06/10/2026, contra 4 h estimadas no backlog.
- **Lição principal:** o protótipo executado antes do *blueprint* evitou os erros típicos de primeira execução: `ResourceWarning`, `tasks.db` criado pelos testes e configuração lida na importação. Com isso, o modelo de execução chegou ao verde em cada passo sem improvisar. As interrupções de API mostraram outro valor do *blueprint* persistido: ele permite retomar o trabalho a partir do disco.

## Entradas da release v0.3.0

### Prompt 25: *blueprint* da `v0.3.0`

- **Data:** 05/10/2026
- **Fase:** planejamento da *release* `v0.3.0`
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - leitura do backlog (RT-05 a RT-09, RF-01 a RF-08), do escopo (D-01 a D-04), dos fluxos e do modelo de dados de `docs/arquitetura.md` e dos Prompts 26 a 31 planejados;
  - protótipo completo fora do repositório, no `.venv` do projeto: 69 testes com `-W error`, mypy sem erros em 17 arquivos e CRUD respondendo no uvicorn;
  - rodada do roteiro de checagem de APIs: `status.HTTP_422_UNPROCESSABLE_ENTITY` emite `StarletteDeprecationWarning` (Starlette 1.7.0) e passou a proibido; `session.query` não emite aviso, mas é estilo legado do SQLAlchemy 2.1.3; `.dict()`, `.from_orm()` e `@validator` emitem `PydanticDeprecatedSince20` (Pydantic 2.13.5);
  - geração de [`docs/blueprint-v030.md`](blueprint-v030.md): D-01 a D-04 com a recomendação do escopo, ADR-14 e ADR-15, DT-04 a DT-08, contrato da API, importações por arquivo, padrões proibidos, seis passos com testes nomeados e contagem esperada por passo.
- **Prompt:** [`prompts/Prompt 25 - blueprint da v0.3.0`](../prompts/Prompt%2025%20-%20blueprint%20da%20v0.3.0)
- **Refinamentos:** aprovado pelo autor sem alteração registrada, incluindo as decisões propostas pelo assistente além de D-01 a D-04 (`extra="forbid"`, `due_at` com fuso obrigatório, título sem espaços nas pontas, `PATCH {}` com `200` e o novo `app/api/error_handlers.py`).
- **Ganho percebido:** ~2,5 h (desenho verificado de treze itens, dois ADRs e cinco DTs)
- **Desafios:**
  - **Erros que só o protótipo mostrou.** `created_at` e `updated_at` diferiam em 1 µs na criação (resolvido pela DT-06), e o mypy recusava o parâmetro `responses` das rotas sem anotação explícita.
  - **Arquivo fora da estrutura.** Os tradutores de exceção não cabiam em nenhum arquivo previsto; o *blueprint* criou `error_handlers.py` dentro de `app/api/`, sem diretório novo, e deixou a atualização da estrutura do `CLAUDE.md` para o fechamento.

### Prompt 26: modelo ORM e esquemas Pydantic

- **Data:** 05/10/2026
- **Fase:** código e testes (`v0.3.0`, passo 1 do *blueprint*)
- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), via Claude Code, como modelo de execução que não participou do desenho
- **Uso da IA:** `utc_now()` e `UTCDateTime` em `base.py`, `task_schemas.py` e `task.py`; DT-04 e DT-05; duas linhas novas no roteiro de checagem do `CLAUDE.md`; 2 testes de persistência (15 no total). Verificou também, fora dos testes previstos, título só com espaços, `id` na entrada, `due_at` sem fuso e `null` no `PATCH`.
- **Prompt:** [`prompts/Prompt 26 - modelo ORM e esquemas Pydantic`](../prompts/Prompt%2026%20-%20modelo%20ORM%20e%20esquemas%20Pydantic)
- **Refinamentos:** nenhum.
- **Ganho percebido:** ~1 h
- **Desafios:** o trecho do *blueprint* omitia as *docstrings* dos métodos do `TypeDecorator`; a IA as acrescentou por exigência do `CLAUDE.md` e registrou o acréscimo.

### Prompt 27: *repository* de tarefas

- **Data:** 05/10/2026
- **Fase:** código e testes (`v0.3.0`, passo 2)
- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), via Claude Code
- **Uso da IA:** `TaskRepository` só com ORM, `commit` seguido de `refresh` nas escritas; 2 testes (17 no total).
- **Prompt:** [`prompts/Prompt 27 - repository de tarefas`](../prompts/Prompt%2027%20-%20repository%20de%20tarefas)
- **Refinamentos:** nenhum.
- **Ganho percebido:** ~0,5 h
- **Desafios:** o *prompt* pedia funções que recebem a sessão como parâmetro, enquanto o *blueprint* define uma classe com a sessão no construtor, e o mesmo *prompt* mandava seguir o *blueprint*. A IA seguiu o *blueprint*, de que dependiam o `TaskStore` e o ADR-14, e registrou a divergência.

### Prompt 28: *service* de tarefas e testes unitários

- **Data:** 05/10/2026
- **Fase:** código e testes (`v0.3.0`, passo 3)
- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), via Claude Code
- **Uso da IA:** `TaskService`, `TaskStore` e `TaskNotFoundError`; dublê `InMemoryTaskRepository` e 14 testes unitários (31 no total); ADR-14, DT-06 e DT-07.
- **Prompt:** [`prompts/Prompt 28 - service de tarefas e testes unitários`](../prompts/Prompt%2028%20-%20service%20de%20tarefas%20e%20testes%20unit%C3%A1rios)
- **Refinamentos:** nenhum.
- **Ganho percebido:** ~1 h
- **Desafios:** nenhum relevante; a IA acrescentou o auxiliar `build_update_body` para não repetir o corpo do `PUT` em dois testes.

### Prompt 29: rotas CRUD e tratamento de erros

- **Data:** 05/10/2026
- **Fase:** código e testes (`v0.3.0`, passo 4)
- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), via Claude Code
- **Uso da IA:** `task_routes.py`, `error_handlers.py` e o registro em `main.py`; 19 funções de teste de integração (38 casos com os parâmetros, 69 no total); ADR-15 e DT-08.
- **Prompt:** [`prompts/Prompt 29 - rotas CRUD e tratamento de erros`](../prompts/Prompt%2029%20-%20rotas%20CRUD%20e%20tratamento%20de%20erros)
- **Refinamentos:** nenhum.
- **Ganho percebido:** ~2 h
- **Desafios:** a primeira tentativa de gravar os testes por *heredoc* extenso foi recusada pelo *shell*, sem efeito; o bloco foi gravado com a ferramenta de escrita.

### Prompt 30: documentação dos endpoints

- **Data:** 06/10/2026
- **Fase:** documentação e execução manual (`v0.3.0`, passo 5)
- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), via Claude Code
- **Uso da IA:**
  - execução da API com banco temporário e chamada de todos os endpoints em Bash (`curl -i`) e em Windows PowerShell 5.1 (`Invoke-RestMethod`), incluindo `404`, `422` e a idempotência da conclusão;
  - verificação, por `TestClient`, do `422` para `id` não numérico nos métodos que o teste não cobria;
  - reescrita da seção Endpoints do README com a tabela de endpoints, os campos da tarefa, os erros e os JSON reais das respostas.
- **Prompt:** [`prompts/Prompt 30 - documentação dos endpoints`](../prompts/Prompt%2030%20-%20documenta%C3%A7%C3%A3o%20dos%20endpoints)
- **Refinamentos:** uma interrupção por erro de API; a retomada corrigiu o script temporário, que estava fora da raiz e não importava `app`.
- **Ganho percebido:** ~1 h
- **Desafios:**
  - **Acentos no Git Bash.** `curl -d` com "relatório" na linha de comando respondeu `400`, e o mesmo corpo por arquivo UTF-8 respondeu `201`. A IA isolou a causa no *shell* (página de código 850), não na API, usou títulos sem acento nos exemplos e registrou a ressalva no README. Uma variante com escape `ó` também falhou e ficou sem explicação.
  - **`503` não reproduzível na API real.** Com a API ligada, o Windows mantém o arquivo do banco bloqueado. O exemplo vem do contrato verificado nos testes, e o README diz isso.
  - **Erro em PowerShell.** `Invoke-RestMethod` lança exceção em `404` e `422`; os exemplos usam `try`/`catch` para mostrar código e corpo.

### Prompt 31: fechamento da `v0.3.0`

- **Data:** 06/10/2026
- **Fase:** documentação e fechamento de *release*
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - README: status, prioridade padrão, data dos exemplos, roadmap com a `v0.3.0` concluída e Uso de IA generativa;
  - `docs/arquitetura.md`: diagramas de módulos, `POST /tasks`, erros em `/tasks/{id}`, modelo de dados e testes ajustados ao código, conferidos contra as importações reais de `app/`; antes e depois em `docs/mermaid.md`;
  - `docs/escopo-mvp.md` com D-01 a D-04 incorporadas aos requisitos; backlog, `CHANGELOG.md`, este histórico, estrutura do `CLAUDE.md`, status do *blueprint* e ordem das DTs em `docs/decisoes.md`.
- **Prompt:** [`prompts/Prompt 31 - fechamento da v0.3.0`](../prompts/Prompt%2031%20-%20fechamento%20da%20v0.3.0)
- **Refinamentos:**
  - uma interrupção por erro de conexão durante o fechamento; retomada a partir do estado em disco;
  - outra queda de conexão logo depois do *push* impediu o relatório final. Numa sessão nova, a IA conferiu o estado publicado, rodou a definição de pronto em clone limpo, validou os diagramas no GitHub e registrou as horas reais informadas pelo autor.
- **Ganho percebido:** ~1,5 h
- **Desafios:**
  - **Validação dos diagramas.** A validação de sintaxe pelo mermaid.ink, usada na `v0.2.0`, foi bloqueada pelo modo automático do Claude Code, por enviar conteúdo a um serviço externo. Depois do *push*, a IA abriu `docs/arquitetura.md` da *tag* `v0.3.0` no GitHub pelo Claude in Chrome. Os seis diagramas renderizaram, sem mensagem de erro de sintaxe.
  - **Horas reais.** O assistente não as mede. O autor informou 4 h para a `v0.2.0` e 8 h para a `v0.3.0`, registradas no backlog. Na `v0.3.0`, cerca de metade do tempo se perdeu com falhas de conexão com a API do Claude, numa internet por *hotspot* compartilhado do celular.
  - **Estado incerto depois de uma queda.** Com a conexão interrompida logo após o *push*, não dava para saber o que tinha sido concluído. A conferência foi feita por fatos verificáveis: *commits*, *branches* e *tag* no `origin` comparados com os locais, clone limpo e renderização no GitHub. O relato da sessão interrompida não serviu de base.
- **Resultado do git:** *commits* `3bff3cb` (*blueprint*), `bf0d6c7` (código) e `f068e6e` (fechamento) na *branch* `feat/crud-tarefas`; *merge* `f1aae05` em `main`; *tag* anotada `v0.3.0` e *push* de `main`, da *tag* e da *branch*. A definição de pronto passou em clone limpo da *tag*: 69 testes, mypy sem erros em 17 arquivos e `git status` limpo. O registro foi feito na *branch* `docs/registro-fechamento-v030`.
  - **Separação dos *commits*.** `docs/arquitetura.md` e `CLAUDE.md` tinham mudanças do código (ADR-14, ADR-15, roteiro de checagem) e do fechamento. As versões anteriores ao fechamento foram guardadas antes das edições, para que cada mudança entre no *commit* a que pertence.

## Release v0.3.0: consolidação

- **Período:** 05 e 06/10/2026 (Prompts 25 a 31)
- **Entregas:** CRUD de tarefas completo. São 6 arquivos novos em `app/` (modelo, esquemas, *repository*, *service*, rotas e tradutores de erro), mais `base.py` e `main.py` alterados. Os testes passam de 13 para 69, com `tests/test_task_service.py` novo. Somam-se o *blueprint* executável, os ADR-14 e ADR-15, cinco DTs, a seção Endpoints com exemplos executados e a *tag* `v0.3.0`.
- **Uso da IA:**
  - repetiu-se a divisão de papéis da `v0.2.0`: o Opus 5.5 desenhou (Prompt 25) e fechou (Prompt 31), e o Sonnet 5.5 executou (Prompts 26 a 30);
  - a execução chegou à contagem de testes prevista em cada passo (15, 17, 31 e 69).
- **Divergências do *blueprint*:**
  - passos 1 a 4: nenhuma de código. Acréscimos registrados: *docstrings* nos métodos do `TypeDecorator`, o auxiliar `build_update_body` e o nome `OLD_TIMESTAMP_TEXT` nos testes;
  - passo 2: o texto do Prompt 27 conflitava com o *blueprint* (funções com sessão × classe); prevaleceu o *blueprint*;
  - passo 5: a API rodou com banco temporário e sem `--reload`, em vez do `DATABASE_URL` padrão; o `404` usa `GET /tasks/999` (e o `DELETE` repetido) em vez do `GET` depois do `DELETE`; o `422` usa título só com espaços e prioridade 9 em vez de `{"title": ""}`; o filtro mostra `?status=done`; os títulos são sem acento; o `503` vem dos testes, não da API real; a seção ganhou as tabelas de campos e de erros;
  - passo 6: a sintaxe dos diagramas não foi validada antes do *push*; as DTs foram reordenadas; o `CLAUDE.md` passou a apontar onde está a rodada de checagem de 05/10/2026.
- **Ganho percebido acumulado:** ~9,5 h (soma das estimativas dos Prompts 25 a 31).
- **Horas reais:** 8 h, informadas pelo autor, contra 6,5 h estimadas no backlog. Segundo o autor, o trabalho caberia em 3 a 4 h. O excedente veio de falhas de conexão com a API do Claude numa internet por *hotspot* compartilhado do celular, que forçaram retomadas de execução.
- **Lição principal:** a execução em ambiente real encontrou o que testes e protótipo não mostram: a página de código do Git Bash, o comportamento do `Invoke-RestMethod` em erro e o bloqueio de arquivo no Windows. Documentar exemplos executados, e não inventados, transformou esses atritos em ressalvas úteis para o avaliador.

## Entradas da release v0.4.0

### Prompt 32: *blueprint* da `v0.4.0`

- **Data:** 06/10/2026
- **Fase:** planejamento da *release* `v0.4.0`
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - leitura do escopo (D-05 a D-07), do backlog com as horas reais, da arquitetura, do código e dos Prompts 33 a 35 planejados;
  - protótipo completo fora do repositório, no `.venv` do projeto: 134 testes com `-W error` e mypy sem erros em 18 arquivos;
  - `docs/blueprint-v040.md` com D-05 a D-07 e D-09, ADR-16 a ADR-18, DT-09 a DT-15, seis passos com testes nomeados, riscos e estimativa de 7,25 h.
- **Prompt:** [`prompts/Prompt 32 - blueprint da v0.4.0`](../prompts/Prompt%2032%20-%20blueprint%20da%20v0.4.0)
- **Refinamentos:**
  - o autor pediu exemplos de tarefas por prioridade e achou o formato ISO de `due_at` difícil de preencher; a IA propôs datas em `DD/MM/AAAA HH:MM` no horário local, com fuso configurável;
  - o autor pediu também aceitar só o dia (`DD/MM/AAAA`), valendo até 23:59; a IA analisou a sugestão, apontou as ressalvas (não fica registrado que só o dia foi informado; ISO só com a data continua recusado) e revisou o *blueprint* com a D-09 e o passo 4 novo.
- **Ganho percebido:** ~3 h
- **Desafios:**
  - **O protótipo encontrou o que a leitura não mostraria.** O `Literal[1, 2, 3, 4]` recusa `?priority=1` na *query string* (DT-12); `ZoneInfo("America/Sao_Paulo")` falha no Windows sem o pacote `tzdata` (DT-14); o Pydantic converte ISO só com a data para 00:00 e aceita `-3` como `timedelta` de 3 segundos (DT-13 e DT-14); um caso de teste da `v0.3.0` (`"10/10/2026"` como data inválida) passaria a ser válido.
  - **Mudança de escopo durante o planejamento.** A D-09 nasceu de uma observação do autor sobre usabilidade, não do backlog. Ela foi tratada como decisão de escopo registrada, com o custo (1,75 h) e a projeção de horas recalculados, e não como ajuste silencioso.

### Prompt 33: `priority_advisor` com funções puras

- **Data:** 06/10/2026
- **Fase:** código e testes (passo 1 do `docs/blueprint-v040.md`)
- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), via Claude Code
- **Uso da IA:**
  - geração de `app/services/priority_advisor.py` (`IncoherentPriorityError`, `ensure_priority_is_coherent`, `suggest_priority`) e de `tests/test_priority_advisor.py` (22 casos), seguindo o código e a tabela de testes do *blueprint*;
  - registro da DT-09 em `docs/decisoes.md`.
- **Prompt:** [`prompts/Prompt 33 - priority_advisor com funções puras`](../prompts/Prompt%2033%20-%20priority_advisor%20com%20fun%C3%A7%C3%B5es%20puras)
- **Refinamentos:** nenhum.
- **Ganho percebido:** ~1 h
- **Desafios:** nenhum erro do modelo; o *blueprint* executável deixou o passo sem decisões em aberto. Definição de pronto na primeira execução: 91 testes e mypy sem erros em 18 arquivos.

### Prompt 34: prioridades no *service* e nas rotas, horário local e exemplos

- **Data:** 06/10/2026
- **Fase:** código, testes e documentação (passos 2 a 5 do `docs/blueprint-v040.md`)
- **Modelo:** Claude Sonnet 5.5 (`claude-sonnet-5-5`), via Claude Code
- **Uso da IA:**
  - geração da integração do `priority_advisor` ao `task_service` (coerência na criação, no `PUT` e no `PATCH`; `build_task_read` com a sugestão), do filtro `?priority=`, do tradutor do `422` e das datas no horário local (`LOCAL_UTC_OFFSET`), seguindo o *blueprint* passo a passo, com a definição de pronto verde a cada passo (100, 114 e 134 testes);
  - registro de DT-10 a DT-15 e ADR-16 a ADR-18;
  - execução da API com banco temporário para obter as respostas reais dos exemplos do README (Bash e PowerShell) e atualização das seções Endpoints e Configuração.
- **Prompt:** [`prompts/Prompt 34 - prioridades no service e nas rotas`](../prompts/Prompt%2034%20-%20prioridades%20no%20service%20e%20nas%20rotas)
- **Refinamentos:** nenhum.
- **Ganho percebido:** ~3,5 h
- **Desafios:**
  - **Divergências pequenas do *blueprint*.** O exemplo de filtro combinado do README passou a `?status=done&priority=1`, para mostrar uma lista não vazia, e os exemplos novos foram executados no fim da sequência; ambas as mudanças estão no README e no arquivo do *prompt*.
  - **`422` de formato de `due_at`.** A união `AwareDatetime | LocalDueAt` gera duas entradas de erro, e o `loc` da segunda traz o nome interno `function-before[parse_local_due_at(), datetime]`. O comportamento foi documentado como é; a decisão de mudá-lo fica com o autor.
  - **Ferramenta de edição.** Um `heredoc` longo com aspas falhou no *shell*; as edições passaram a ser feitas por *scripts* em Python no diretório temporário, preservando o fim de linha CRLF dos arquivos.

### Prompt 35: fechamento da `v0.4.0`

- **Data:** 06/10/2026
- **Fase:** documentação e fechamento de *release*
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - README: status (todos os requisitos funcionais implementados), escopo do MVP sem "por exemplo" no `priority_advisor`, roadmap com a `v0.4.0` concluída, Uso de IA generativa e limitações (fuso fixo, perda do "só o dia", sugestão variável no tempo, `422` de formato com duas entradas);
  - `docs/arquitetura.md`: diagramas de módulos, de `POST /tasks` e do modelo de dados ajustados ao código, conferidos contra as importações reais de `app/`; antes e depois em `docs/mermaid.md`, gerados por *script* que confere se o depois destacado, sem o destaque, é igual à versão oficial;
  - `docs/escopo-mvp.md` com D-05 a D-07 e D-09 incorporadas e RF-14 incluído; backlog, `CHANGELOG.md`, este histórico e o status do *blueprint*.
- **Prompt:** [`prompts/Prompt 35 - fechamento da v0.4.0`](../prompts/Prompt%2035%20-%20fechamento%20da%20v0.4.0)
- **Refinamentos:** nenhum até o relatório.
- **Ganho percebido:** ~1,5 h
- **Desafios:**
  - **Arquivo do *prompt* vazio.** O arquivo `prompts/Prompt 35 - fechamento da v0.4.0` existia sem conteúdo. A IA usou o texto planejado em `prompts/prompts-desenvolvimento.md` e o gravou no arquivo, informando o autor.
  - **Horas reais.** O assistente não as mede. O autor informou 3 h para a `v0.4.0`, registradas no backlog.
  - **Sintaxe dos diagramas.** Sem validação externa antes do *push*, a conferência foi feita depois, no GitHub, pelo Claude in Chrome: os diagramas alterados renderizaram sem erro.
- **Resultado do git:** *commits* `3961430` (*blueprint*), `9291ec1` (código) e `65390be` (fechamento) na *branch* `feat/priority-advisor`; *merge* `d7aba86` em `main`; *tag* anotada `v0.4.0` e *push* de `main`, da *tag* e da *branch*. A definição de pronto passou em clone limpo da *tag*: 134 testes, mypy sem erros em 18 arquivos e `git status` limpo. O registro foi feito na *branch* `docs/registro-fechamento-v040`.

## Release v0.4.0: consolidação

- **Período:** 06/10/2026 (Prompts 32 a 35)
- **Entregas:** `priority_advisor` com funções puras; coerência entre prioridade 4 e `due_at` na criação, no `PUT` e no `PATCH`, com `422` em texto; `suggested_priority` em todas as respostas; filtro `?priority=` (RF-14); `due_at` em `DD/MM/AAAA HH:MM` ou `DD/MM/AAAA` no horário local e datas devolvidas no fuso de `LOCAL_UTC_OFFSET` (D-09). Os testes passam de 69 para 134, com `tests/test_priority_advisor.py` novo. Somam-se os ADR-16 a ADR-18, as DT-09 a DT-15 e os exemplos do README executados na API.
- **Uso da IA:**
  - manteve-se a divisão de papéis: o Opus 5.5 desenhou (Prompt 32) e fechou (Prompt 35), e o Sonnet 5.5 executou (Prompts 33 e 34);
  - a execução chegou à contagem de testes prevista em cada passo (91, 100, 114 e 134), sem erro de teste ou de mypy em nenhum passo.
- **Divergências do *blueprint*:**
  - passos 1 a 4: nenhuma de código;
  - passo 5: o exemplo de filtro combinado do README usa `?status=done&priority=1` (lista não vazia), e os exemplos novos foram executados no fim da sequência, o que o README informa;
  - passo 6: o README ganhou duas limitações além das previstas (sugestão variável no tempo e `422` de formato com duas entradas); os diagramas de erros em `/tasks/{id}` e de testes não mudaram, só o texto das seções; a sintaxe dos diagramas alterados não foi validada antes do *push* (a validação externa ficou bloqueada na `v0.3.0`); foi conferida depois, no GitHub, sem erro.
- **Ganho percebido acumulado:** ~9 h (soma das estimativas dos Prompts 32 a 35).
- **Horas reais:** 3 h, informadas pelo autor, contra 7,25 h estimadas (5,75 h dos itens, mais *blueprint* e fechamento). Foi a primeira *release* abaixo da estimativa; a projeção do projeto caiu para cerca de 22 h.
- **Lição principal:** o *blueprint* executável, com protótipo prévio, transferiu o risco para o planejamento: os seis problemas encontrados no protótipo (formato da *query string*, base de fusos no Windows, conversões do Pydantic, teste antigo invalidado) foram resolvidos antes da execução, e o modelo de execução seguiu os passos sem improvisar. A mudança de escopo pedida pelo autor (D-09) entrou pelo mesmo caminho: decisão registrada, custo estimado e testes previstos.

## Entradas da release v0.5.0

### Prompt 36: *blueprint* da `v0.5.0`

- **Data:** 06/10/2026
- **Fase:** planejamento da *release* `v0.5.0` (revisão)
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - leitura do backlog (RT-11 a RT-14), das DT-01 a DT-15, dos ADR-01 a ADR-18 e dos Prompts 37 a 40 planejados;
  - levantamento prévio no código, para que o *blueprint* não deixasse decisões em aberto: importações por camada, tamanho das funções, SQL textual, testes de erro existentes e conversões em `app/models/`;
  - `docs/blueprint-v050.md`: ordem das revisões, critérios copiados do backlog, forma do checklist, regra de decisão entre código e documento, critério de promoção de DT a ADR já aplicado (ADR-19 e ADR-20), limites, condição de parada e estimativa (4 h).
- **Prompt:** [`prompts/Prompt 36 - blueprint da v0.5.0`](../prompts/Prompt%2036%20-%20blueprint%20da%20v0.5.0)
- **Refinamentos:** nenhum; aprovado pelo autor ao pedir o Prompt 37.
- **Ganho percebido:** ~1 h
- **Desafios:**
  - **Regra genérica contra código real.** O `CLAUDE.md` diz "modelos sem lógica", e o código tem três conversões em `app/models/`. A IA não as tratou como desvio a corrigir: propôs registrar a exceção (ADR-20), porque movê-las mudaria o contrato do `422`.
  - **Detalhe interno no `422`.** O nome `parse_local_due_at` no `loc` foi classificado pela regra escrita (*stack trace*, SQL, caminho) e não por impressão, com a decisão (R-05) deixada para o autor confirmar.

### Prompt 37: revisão de arquitetura

- **Data:** 06/10/2026
- **Fase:** revisão (passo 1 do `docs/blueprint-v050.md`, RT-11)
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - comparação automática (*script* com `ast`) das 28 importações internas de `app/` com as arestas do diagrama de módulos, sem divergência;
  - contagem de linhas por função, de *docstrings* e levantamento dos nomes de variáveis;
  - checklist de 16 verificações com evidência; ADR-19 e ADR-20, citações nos ADR-15 e ADR-17, DTs marcadas como promovidas e diagrama de módulos com o antes e o depois em `docs/mermaid.md`.
- **Prompt:** [`prompts/Prompt 37 - revisão de arquitetura`](../prompts/Prompt%2037%20-%20revis%C3%A3o%20de%20arquitetura)
- **Refinamentos:** nenhum.
- **Ganho percebido:** ~1 h
- **Desafios:**
  - **Nenhum desvio de código.** As camadas foram respeitadas desde a `v0.2.0`; o resultado da revisão foi só documental. A comparação por *script*, e não por leitura, dá a evidência de que nenhuma importação ficou de fora.
  - **Edição por *script*.** A inserção das linhas "Promovida" falhou na DT-13, que tem a mesma linha de IDs da DT-14; a edição passou a ser feita pela posição de cada DT, sem efeito parcial no arquivo.

### Prompt 38: revisão de segurança

- **Data:** 07/10/2026
- **Fase:** revisão (passo 2 do `docs/blueprint-v050.md`, RT-12)
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - buscas por SQL textual e strings formatadas em `app/`; leitura de rotas, esquemas, tradutores de erro e chamadas de log;
  - sondagem por *script* temporário, fora do repositório, das respostas de erro em `production` e do conteúdo do log de uma falha real do banco;
  - duas correções: `task_id` limitado a `2**63 - 1` (`TaskId`, DT-16), que respondia `500` não tratado (`OverflowError` do driver), e `hide_parameters=True` no engine (DT-17), porque o log trazia o título e a descrição enviados;
  - três testes novos (9 casos), dois deles conferidos em vermelho contra o código do `HEAD`; varredura de segredos no histórico sem achados; checklist de 17 verificações.
- **Prompt:** [`prompts/Prompt 38 - revisão de segurança`](../prompts/Prompt%2038%20-%20revis%C3%A3o%20de%20seguran%C3%A7a)
- **Refinamentos:** três interações seguintes. O autor pediu para rodar o mypy no WSL; a IA verificou que o WSL não tinha distribuição instalada e apresentou o que a instalação exigiria (usuário Linux interativo, outra versão do Python). O autor decidiu não usar mais o mypy: ADR-21, mypy e as dependências que só ele usava retirados do `requirements.txt`, do `.venv` e da definição de pronto (`CLAUDE.md`, README, escopo, backlog e *blueprint* da `v0.5.0`). Depois, a pedido do autor, a IA testou o mypy 1.18.2 em Python puro, e o autor registrou a checagem como bem-sucedida (ver Desafios).
- **Ganho percebido:** ~1 h
- **Desafios:**
  - **Sondar em vez de só ler.** Nenhum dos dois desvios aparece na leitura do código nem nos testes existentes: o `OverflowError` vem do driver, e os parâmetros entram no log pela mensagem padrão da exceção do SQLAlchemy. Ambos foram achados executando a API com entradas extremas e lendo o log produzido.
  - **Definição de pronto bloqueada pelo ambiente.** O Smart App Control passou a bloquear os `.pyd` do mypy 2.4.0 e do `librt`, que tinham rodado no dia anterior. O mypy em Python puro também falhou, porque o `librt` só existe compilado. A checagem de tipos ficou pendente, com a decisão para o autor, que retirou o mypy do projeto (ADR-21): desligar o Smart App Control é irreversível, e o WSL exigiria instalar e manter um segundo ambiente fora do Windows com PowerShell. A tipagem passa a ser conferida na revisão de código. A pedido do autor, a IA procurou alternativa não binária: o mypy 1.18.2, última versão sem o `librt`, tem pacote em Python puro e não é bloqueado. Executado fora do repositório sobre o código do Prompt 38, terminou com sucesso (18 arquivos sem erros) em 6 de 12 execuções; nas outras 6, o interpretador Python 3.14.6 caiu com erro interno (`Executing a cache`), sem apontar erro de tipo. O autor considerou as execuções bem-sucedidas suficientes como evidência da checagem.

### Prompt 39: revisão da documentação e das dependências

- **Data:** 07/10/2026
- **Fase:** revisão (passos 3 e 4 do `docs/blueprint-v050.md`, RT-14 e RT-13)
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - consulta à API JSON do PyPI das 7 dependências diretas e à base OSV dos 26 pacotes fixados; leitura das notas de versão do FastAPI 0.142.3 e do SQLAlchemy 2.1.4, publicadas no dia; `pip check` e comparação do `pip freeze` com o `requirements.txt`;
  - execução, por *script* PowerShell fora do repositório, dos exemplos do README contra a API com banco temporário (31 requisições), e da seção Configuração (`production`, valores inválidos, outro fuso, `.env`, `--reload`);
  - contagem de *docstrings* por `ast`; comparação por *script* dos diagramas oficiais com o catálogo `docs/mermaid.md` e das importações com o diagrama de módulos;
  - checklist de 21 verificações; quatro ajustes de texto em `docs/arquitetura.md` (`TaskId`, `hide_parameters`, contagem de testes, assinatura no ADR-14) e um em `docs/escopo-mvp.md` (origem da D-08).
- **Prompt:** [`prompts/Prompt 39 - revisão da documentação e das dependências`](../prompts/Prompt%2039%20-%20revis%C3%A3o%20da%20documenta%C3%A7%C3%A3o%20e%20das%20depend%C3%AAncias)
- **Refinamentos:** nenhum.
- **Ganho percebido:** ~1 h
- **Desafios:**
  - **Versões novas no dia da revisão.** O FastAPI 0.142.3 e o SQLAlchemy 2.1.4 saíram horas antes da consulta. A decisão seguiu a R-06 do *blueprint*: nenhuma vulnerabilidade na OSV e nenhuma correção com efeito observável no projeto (os 143 testes passam com `-W error`). Ficaram registradas como "disponível, não adotada", com o motivo de cada uma.
  - **Exemplos em PowerShell e corpo da resposta.** O `Invoke-RestMethod` não mostra a lista vazia (`[]`) nem o `204`; o corpo bruto e os códigos de sucesso foram conferidos com `Invoke-WebRequest`. Nenhum exemplo divergiu: o README não mudou além das datas.
  - **Documentação defasada pelo prompt anterior.** As correções de segurança do Prompt 38 (`TaskId`, `hide_parameters`, 9 testes) não tinham chegado à seção de módulos nem à de testes da arquitetura; só a comparação do texto com o código mostrou a defasagem.

### Prompt 40: fechamento da `v0.5.0`

- **Data:** 07/10/2026
- **Fase:** documentação e fechamento de *release* (passo 5 do `docs/blueprint-v050.md`)
- **Modelo:** Claude Opus 5.5 (`claude-opus-5-5`), via Claude Code
- **Uso da IA:**
  - README: status com a `v0.5.0` concluída e o que a revisão mudou, roadmap, Uso de IA generativa (Prompts 36 a 40), lista de *blueprints* e duas limitações (nome do validador no `loc` do `422` de formato, pela R-05; ausência de checagem de tipos por ferramenta, ADR-21);
  - `CLAUDE.md` corrigido onde a revisão o mostrou divergente: `app/models/` com conversões de formato e sem regra de negócio (ADR-20), promoção de DTs já feita, `error_handlers.py` com o `422` de coerência, `TaskId` na estrutura, rodada do roteiro de 07/10/2026 sem mudança;
  - backlog com RT-11 a RT-14 concluídos e as horas reais; escopo com status e rastreabilidade atualizados; `CHANGELOG.md` com a seção `0.5.0`, completada com as linhas dos Prompts 36 e 37 que faltavam; status do *blueprint*; consolidação da *release*.
- **Prompt:** [`prompts/Prompt 40 - fechamento da v0.5.0`](../prompts/Prompt%2040%20-%20fechamento%20da%20v0.5.0)
- **Refinamentos:** a IA pediu ao autor as horas reais da *release* antes de atualizar o backlog.
- **Ganho percebido:** ~1,5 h
- **Desafios:**
  - **Pendências de fechamentos anteriores.** O status de `docs/escopo-mvp.md` ainda citava só as decisões da `v0.3.0`, e o comentário de `error_handlers.py` na estrutura do `CLAUDE.md` não citava o `422` de coerência da `v0.4.0`. Ambos foram achados ao reler os arquivos por inteiro, e não só as seções previstas.
  - **R-05 sem registro.** O *blueprint* dizia que o nome `parse_local_due_at` no `422` ficaria "documentado nas Limitações do README", mas nenhum passo anterior o fez; a limitação entrou no fechamento.

## Release v0.5.0: consolidação

- **Período:** 06 e 07/10/2026 (Prompts 36 a 40)
- **Entregas:** revisões de arquitetura (RT-11), segurança (RT-12), dependências (RT-14) e documentação (RT-13), cada uma com checklist e evidência no arquivo do *prompt*. Sem funcionalidade nova. A arquitetura não tinha desvio de código; as DTs estruturais viraram ADR-19 e ADR-20. A segurança corrigiu dois desvios achados por sondagem da API em execução: `id` acima do maior inteiro do SQLite respondia `500` não tratado (DT-16) e o log de falha do banco trazia os dados enviados pelo cliente (DT-17); os testes passaram de 134 para 143. As dependências não mudaram (R-06), e os exemplos do README conferiram com a API.
- **Uso da IA:**
  - o Opus 5.5 fez o planejamento, as quatro revisões e o fechamento; não houve modelo de execução separado, porque a revisão exige julgamento a cada verificação;
  - as verificações foram feitas por *script* sempre que possível (importações contra o diagrama, *docstrings* por `ast`, diagramas contra o catálogo, exemplos do README contra a API), o que deixa evidência reproduzível em vez de impressão de leitura.
- **Divergências do *blueprint*:**
  - passo 1: nenhuma;
  - passo 2: a correção do `task_id` mudou o comportamento da API (`500` para `422`), o que a seção 4, item 1, não prevê; foi feita pelo pedido explícito do Prompt 38 e pelo contrato do ADR-15, e registrada no `CHANGELOG.md`. O mypy deixou de rodar por bloqueio do ambiente e saiu do projeto por decisão do autor (ADR-21), com o *blueprint* ajustado;
  - passos 3 e 4: nenhuma;
  - passo 5: além do previsto, o `CLAUDE.md` também foi corrigido no comentário de `error_handlers.py`, na regra de promoção de DTs e no `TaskId`; o status do escopo, defasado desde a `v0.4.0`, foi atualizado; a limitação da R-05 entrou no README só no fechamento.
- **Ganho percebido acumulado:** ~5,5 h (soma das estimativas dos Prompts 36 a 40).
- **Horas reais:** 4 h, informadas pelo autor, iguais à estimativa (2,5 h dos itens, mais *blueprint* e fechamento). Até a `v0.5.0`, 19 h contra 20,75 h estimadas; a projeção do projeto continua em cerca de 22 h.
- **Lição principal:** revisar lendo o código não bastou. Os dois desvios de segurança não apareciam no código nem nos testes: um vinha do *driver* e o outro da mensagem padrão da exceção do SQLAlchemy. Só apareceram ao executar a API com entradas extremas e ler o log produzido. Do mesmo modo, a documentação defasada pelas próprias correções só apareceu ao comparar o texto com o código, item a item.

## Observações transversais

Padrões que se repetiram nas interações até aqui, a aprofundar na análise final:

- **O `CLAUDE.md` funcionou como contrato.** Vários *prompts* pediam algo em conflito com regras já acordadas (Node.js, priorização por IA, arquivos fora da estrutura). A IA não escolheu sozinha: aplicou a regra, apontou a divergência e devolveu a decisão ao autor.
- **Verificação por execução supera o conhecimento do modelo.** O caso `httpx2` mostra que versões e APIs mudam depois do corte de treinamento; consultar o PyPI e rodar código no ambiente real evitou um erro que só apareceria nos testes.
- **Premissas erradas nos *prompts* foram detectadas, não completadas.** Arquivos inexistentes, roadmap inexistente e códigos HTTP impossíveis no fluxo pedido foram apontados antes de a IA produzir conteúdo sobre eles.
- **A IA também erra.** O `.gitignore` do Prompt 00 tinha um padrão que ignorava o `.env.example`; a revisão seguinte corrigiu. Por isso toda saída passa por revisão antes de entrar em `main`.
- **Ambiente Windows gera atritos próprios:** bloqueio de arquivo aberto em outro programa e conversão de fim de linha (LF/CRLF), tratados sem perda de dados. O Smart App Control bloqueou extensões compiladas não assinadas: as do SQLAlchemy, contornadas com a instalação em Python puro, e as do mypy, que saiu do projeto (ADR-21).
