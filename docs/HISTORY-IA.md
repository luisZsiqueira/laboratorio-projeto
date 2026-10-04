# Histórico do uso de IA generativa

Registro cronológico de como a IA generativa foi usada no desenvolvimento do projeto: em que fase do ciclo de vida, com que *prompt*, com que ganho e com que dificuldades. É a base do histórico de uso de IA exigido pelo curso e permite, ao final, uma leitura acadêmica do processo.

## Como ler este arquivo

- Cada entrada corresponde a uma interação relevante e referencia o arquivo do *prompt* em [`prompts/`](../prompts/), onde estão o texto enviado e o registro da execução.
- Campos de cada entrada: data, fase do ciclo de vida, modelo/assistente, como a IA foi usada, *prompt* aplicado, refinamentos, ganho percebido e desafios.
- O **ganho percebido** é uma estimativa das horas que a mesma tarefa levaria sem IA, menos o tempo efetivamente gasto. É uma percepção, não uma medição, e deve ser lida como ordem de grandeza.
- Toda saída da IA foi revisada pelo autor antes de entrar na *branch* `main`. As decisões de escopo ficaram com o humano.

## Ambiente

| Item | Valor |
| --- | --- |
| Assistente | Claude Code (CLI), no VS Code, em Windows 11 com PowerShell |
| Modelo | Claude Opus 5.5 (`claude-opus-5-5`) |
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

## Entradas

### Prompt 00: estrutura e repositório

- **Data:** 03/10/2026
- **Fase:** planejamento e configuração do ambiente
- **Modelo:** Claude Opus 5.5, via Claude Code
- **Uso da IA:** geração da estrutura de diretórios a partir do `CLAUDE.md`, criação do `.gitignore` inicial, `git init` em `main` e primeiro *commit*
- **Prompt:** [`prompts/Prompt00 - Inicio`](../prompts/Prompt00%20-%20Inicio)
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

## Observações transversais

Padrões que se repetiram nas interações até aqui, a aprofundar na análise final:

- **O `CLAUDE.md` funcionou como contrato.** Vários *prompts* pediam algo em conflito com regras já acordadas (Node.js, priorização por IA, arquivos fora da estrutura). A IA não escolheu sozinha: aplicou a regra, apontou a divergência e devolveu a decisão ao autor.
- **Verificação por execução supera o conhecimento do modelo.** O caso `httpx2` mostra que versões e APIs mudam depois do corte de treinamento; consultar o PyPI e rodar código no ambiente real evitou um erro que só apareceria nos testes.
- **Premissas erradas nos *prompts* foram detectadas, não completadas.** Arquivos inexistentes, roadmap inexistente e códigos HTTP impossíveis no fluxo pedido foram apontados antes de a IA produzir conteúdo sobre eles.
- **A IA também erra.** O `.gitignore` do Prompt 00 tinha um padrão que ignorava o `.env.example`; a revisão seguinte corrigiu. Por isso toda saída passa por revisão antes de entrar em `main`.
- **Ambiente Windows gera atritos próprios:** bloqueio de arquivo aberto em outro programa e conversão de fim de linha (LF/CRLF), tratados sem perda de dados.
