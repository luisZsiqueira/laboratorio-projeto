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

## Observações transversais

Padrões que se repetiram nas interações até aqui, a aprofundar na análise final:

- **O `CLAUDE.md` funcionou como contrato.** Vários *prompts* pediam algo em conflito com regras já acordadas (Node.js, priorização por IA, arquivos fora da estrutura). A IA não escolheu sozinha: aplicou a regra, apontou a divergência e devolveu a decisão ao autor.
- **Verificação por execução supera o conhecimento do modelo.** O caso `httpx2` mostra que versões e APIs mudam depois do corte de treinamento; consultar o PyPI e rodar código no ambiente real evitou um erro que só apareceria nos testes.
- **Premissas erradas nos *prompts* foram detectadas, não completadas.** Arquivos inexistentes, roadmap inexistente e códigos HTTP impossíveis no fluxo pedido foram apontados antes de a IA produzir conteúdo sobre eles.
- **A IA também erra.** O `.gitignore` do Prompt 00 tinha um padrão que ignorava o `.env.example`; a revisão seguinte corrigiu. Por isso toda saída passa por revisão antes de entrar em `main`.
- **Ambiente Windows gera atritos próprios:** bloqueio de arquivo aberto em outro programa e conversão de fim de linha (LF/CRLF), tratados sem perda de dados.
