# Pré-história do uso de IA generativa

Registro do uso de IA **anterior ao repositório**: a concepção do `CLAUDE.md` inicial, feita fora do Claude Code. Complementa o [`docs/HISTORY-IA.md`](HISTORY-IA.md), que começa no Prompt 00, em 03/10/2026, quando o projeto foi iniciado de fato no Claude Code.

> **Fonte:** declaração do autor, registrada em 04/10/2026 (Prompt 13). As sessões descritas aqui não deixaram registro no repositório; não há *prompts*, respostas nem estimativas de ganho a citar.

## Resumo

| Item | Valor |
| --- | --- |
| Período | 01/10/2026 e 02/10/2026 |
| Ferramenta | Claude, em modo *chat* |
| Modelo | Claude Opus 5.5 |
| Condução | o aluno, autor do projeto |
| Entrada | capturas de tela do curso C4-LICMIAG da pós-graduação SWE-GENAI, com os requisitos de submissão do miniprojeto, e as características gerais do MVP |
| Saída | o `CLAUDE.md` inicial, arquivo que define o contexto do projeto e foi o primeiro a existir no repositório |
| Registro no repositório | nenhum; as sessões ocorreram antes de o projeto existir no Claude Code |

## O que aconteceu

1. **Requisitos do curso.** O aluno forneceu ao *chat* capturas de tela do curso C4-LICMIAG com os requisitos de submissão do miniprojeto. Esses requisitos foram depois transcritos para [`docs/requerimentos.md`](requerimentos.md), quando o arquivo foi criado (ver Prompt 02 no histórico).
2. **Características do MVP.** O aluno descreveu as características gerais do MVP, que aparecem na seção "Ponto de partida" do `CLAUDE.md` inicial.
3. **`CLAUDE.md` inicial.** A partir dessas entradas, o aluno formou o `CLAUDE.md` com apoio do *chat*. A versão que entrou no primeiro *commit* (`94f30f2`) já tinha as seções de papel e contexto, fontes de verdade, ponto de partida, inicialização do projeto, forma de trabalhar, Git, convenções de código, testes, segurança, estrutura de diretórios e ambiente de desenvolvimento. Esse arquivo deu início ao repositório no Prompt 00.

## Por que não há registro detalhado

- As sessões aconteceram no *chat*, e não no ambiente em que o projeto é versionado. O projeto só passou a existir de fato no Claude Code, em 03/10/2026.
- Por isso, não há arquivos em `prompts/` para esse período, e as regras de registro do `CLAUDE.md` (que nasceram nessas mesmas sessões) ainda não estavam em vigor.
- Este arquivo não reconstrói o conteúdo das conversas. Registra apenas o que o autor declarou, para que o histórico de uso de IA não comece com uma lacuna sem explicação.

## Leitura para o histórico do curso

- A IA generativa foi usada desde a **concepção**, antes de qualquer arquivo: na leitura dos requisitos do curso e na definição das regras de trabalho com o assistente.
- O `CLAUDE.md` produzido nessa fase funcionou como contrato nas interações seguintes. O [`docs/HISTORY-IA.md`](HISTORY-IA.md) (Observações transversais) mostra como ele orientou o assistente e evitou ampliações de escopo.
- A evolução do `CLAUDE.md` a partir do repositório pode ser acompanhada pelo histórico do git (`git log -- CLAUDE.md`).
