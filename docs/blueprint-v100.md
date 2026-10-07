# Blueprint da `v1.0.0`: entrega do curso

> **Status:** executado. Proposto em 07/10/2026 (Prompt 41) e aprovado pelo autor; executado pelos Prompts 42 (passo 1), 43 (passo 2) e 44 (passo 3, publicação e fechamento), em 07/10/2026. A *release* `v1.0.0` foi publicada com *tag* e *Release* no GitHub. Quem executa lê este arquivo e o `CLAUDE.md`; nada depende do histórico do *chat*.

## 1. Escopo da *release*

Validação, documentação e publicação, sem código novo. Os critérios de aceite são os de `docs/backlog.md` (seção 4.5), copiados abaixo, mais os critérios comuns do backlog (seções 2 e 2.1).

| Passo | ID | Item | Critérios de aceite (backlog) | Prompt |
| --- | --- | --- | --- | --- |
| 1 | RT-15 | Validação em máquina limpa | 1. Clone novo, `.venv` novo e instalação só com os comandos do README **[C]**<br>2. API sobe e responde em `/health` e nos exemplos do README **[C]**<br>3. Definição de pronto passa no clone **[C]**<br>4. Execução feita em PowerShell; Bash conferido no Git Bash ou registrado como não verificado **[C]** | 42 |
| 2 | RT-16 | Histórico de uso de IA consolidado | 1. `docs/HISTORY-IA.md` com todas as entradas, consolidação por *release* e análise final **[I]**<br>2. README (Uso de IA generativa) lista todos os assistentes, modelos e etapas **[I]**<br>3. Todo *prompt* de `prompts/` tem o registro da execução **[I]** | 43 |
| 3 | RT-17 | Publicação da entrega | 1. Rastreabilidade com os requisitos do curso (seção 7 do escopo) toda como atendida **[I]**<br>2. Status do README como "concluído" na `v1.0.0` **[I]**<br>3. *Tag* `v1.0.0` publicada e *Release* criada no GitHub com o texto do `CHANGELOG.md` **[C]** | 44 |

**Ordem e motivo.** A validação vem primeiro, porque é a única que pode mudar o README (Como rodar). O histórico vem depois, para registrar a validação. A publicação vem por último, porque a rastreabilidade e o `CHANGELOG.md` dependem dos dois passos anteriores.

## 2. Levantamento prévio (07/10/2026)

Feito antes deste *blueprint*, para que ele não deixe decisões em aberto:

| Verificação | Resultado |
| --- | --- |
| Definição de pronto em `main` (`6ae17f4`, igual a `origin/main`) | `143 passed`, sem avisos |
| *Tags* publicadas | `v0.1.0` a `v0.5.0` |
| *Commits* no padrão *Conventional Commits* | 33 de 48 (os demais são *merges* com a mensagem padrão do git) |
| Registro da execução em `prompts/` | presente nos Prompts 00 a 08, 10 a 13 e 20 a 40; ausente nos Prompts 41 a 44 (ainda não executados) |
| Numeração de `prompts/` | não existem os Prompts 09 e 14 a 19; o `docs/HISTORY-IA.md` explica só o 09 |
| `docs/HISTORY-IA.md`, tabela Ambiente | a linha Modelo cita os modelos só até o Prompt 31 |
| `docs/EXTRA-HISTORY-IA.md`, R-01 | o *link* para o `HISTORY-IA.md` é um caminho local (`file:///C:/...`), quebrado no GitHub |
| `prompts/prompts-desenvolvimento.md` | status "proposta para revisão do autor"; a definição de pronto citada inclui o mypy, retirado pelo ADR-21 |
| GitHub CLI (`gh`) | não instalado nesta máquina |
| `winget` | não encontrado nesta máquina |
| WSL | instalado, sem distribuição Linux |
| Git Bash | disponível; `python3` resolve para o Python 3.14.6 |
| `.gitignore` | ignora `.env`, `*.db`, `.venv/`, `.pytest_cache/` e `__pycache__/` |

## 3. Decisões tomadas

Não há decisão em aberto. As decisões abaixo são confirmadas na aprovação.

| ID | Decisão | Motivo |
| --- | --- | --- |
| E-01 | O Prompt 42 clona `https://github.com/luisZsiqueira/laboratorio-projeto.git` (`main`), como faria o avaliador. O Prompt 44 repete a validação em PowerShell no clone da *tag* `v1.0.0`, depois do *push* | valida o que está publicado; as correções do passo 1 só chegam ao GitHub no passo 3 |
| E-02 | Diretórios de validação: `$env:TEMP\validacao-v100-ps` (PowerShell) e `"$TEMP/validacao-v100-bash"` (Git Bash), criados vazios e removidos ao final de cada execução | fora do repositório; uma execução por *shell*, sem estado compartilhado |
| E-03 | Bash conferido no Git Bash do Windows. O README indica `source .venv/bin/activate` (Linux/macOS), que não existe no Windows; no Git Bash, a ativação é `source .venv/Scripts/activate`. O passo 2 do Como rodar em Linux/macOS fica registrado como **não verificado** (sem máquina Linux nem distribuição WSL) | RT-15, critério 4, admite o registro como não verificado; não se instala distribuição Linux para a entrega |
| E-04 | O README (Como rodar) ganha duas linhas para o Git Bash do Windows: a ativação `source .venv/Scripts/activate` no passo 2, e a forma Bash da Solução de problemas (`DISABLE_SQLALCHEMY_CEXT=1 python -m pip install --force-reinstall --no-deps --no-binary SQLAlchemy SQLAlchemy==2.1.3`) | o avaliador em Windows pode usar Git Bash; o `CLAUDE.md` exige os comandos em PowerShell e em Bash |
| E-05 | Se o Smart App Control bloquear o SQLAlchemy no `.venv` novo, aplica-se a Solução de problemas do README, e isso não conta como falha do README. Conta como falha só um comando do README que não funcione como descrito | o bloqueio é do ambiente desta máquina (`CLAUDE.md`, Ambiente de desenvolvimento) e já está documentado |
| E-06 | Exemplos de API: em PowerShell, `/health` e todos os exemplos da seção Endpoints, na ordem do README; em Git Bash, `/health`, o primeiro exemplo de `POST /tasks` e `GET /tasks`. Instantes, `id` e `suggested_priority` mudam com a execução e não contam como divergência; código HTTP e forma do corpo contam | os exemplos completos já foram conferidos em PowerShell no Prompt 39; o Git Bash confere o caminho Bash |
| E-07 | Nenhuma versão de dependência muda na `v1.0.0` e não há nova rodada do roteiro de APIs deprecadas: as versões foram conferidas em 07/10/2026 (Prompt 39). Se a instalação falhar por versão indisponível, vale a condição de parada | estabilidade da entrega; mudar versão exige justificativa e fonte (`CLAUDE.md`) |
| E-08 | Tratamento das lacunas do histórico: (a) o que está registrado nos arquivos é consolidado; (b) o que só o autor sabe (horas reais, motivo da numeração) é perguntado ao autor; (c) o que não tem fonte fica escrito como "não registrado". Nenhuma conversa é reconstruída | `CLAUDE.md`, Idioma e comunicação: distinguir fato de estimativa; Prompt 43, Estilo |
| E-09 | `docs/EXTRA-HISTORY-IA.md`: só o *link* do R-01 muda, de `file:///C:/...` para o caminho relativo `HISTORY-IA.md`; o texto do autor fica como está | *link* quebrado no repositório público; o arquivo é registro do autor |
| E-10 | `prompts/prompts-desenvolvimento.md`: só a linha de status muda, para "executado (Prompts 21 a 44, 05 a dd/10/2026)", com a nota de que o mypy citado nos *prompts* foi retirado pelo ADR-21. Os textos dos *prompts* não mudam | os textos são o registro do que foi planejado |
| E-11 | Análise final: nova seção "Análise final" ao fim de `docs/HISTORY-IA.md`, depois de "Observações transversais", com ganho percebido acumulado (soma das estimativas, marcada como estimativa), horas reais totais, principais desafios, decisões que ficaram com o humano e lições | RT-16, critério 1; Prompt 43 |
| E-12 | *Release* no GitHub com a GitHub CLI: `gh release create v1.0.0 --title "v1.0.0" --notes-file <arquivo>`, em que `<arquivo>` é um arquivo temporário em `$env:TEMP` com o texto da seção `[1.0.0]` do `CHANGELOG.md`, sem a linha do título. A `gh` é ferramenta da máquina do autor, não dependência do projeto: não entra no `requirements.txt` nem no README. Instalação e autenticação (`! gh auth login`) ficam com o autor, antes do Prompt 44 | Prompt 44 pede `gh release create`; a autenticação é interativa e envolve credenciais |
| E-13 | Status final do README: "**Status:** concluído. Entregue na `v1.0.0` (dd/10/2026)…", seguido do resumo do que existe; Roadmap com a `v1.0.0` "concluída (dd/10/2026, *tag* e *Release* `v1.0.0`)" | RT-17, critério 2 |
| E-14 | *Commits* na *branch* `docs/entrega-v100`, um por *prompt*, todos do tipo `docs` (o Prompt 42 só altera o README): `docs: adiciona o blueprint da v1.0.0`, `docs: registra a validação em máquina limpa`, `docs: consolida o histórico de uso de IA`, `docs: fecha a release v1.0.0`. *Commit* só quando pedido | `CLAUDE.md`, Git |
| E-15 | Modelos sugeridos: Prompt 42 com o Claude Sonnet 5.5 (roteiro mecânico, com condição de parada); Prompts 43 e 44 com o Claude Opus 5.5 (julgamento sobre lacunas e rastreabilidade) | `prompts/prompts-desenvolvimento.md`, Modelo sugerido |

## 4. Passos

Estado inicial: `main` em `6ae17f4`, 143 testes, definição de pronto verde. Cada passo termina com `python -m pytest -W error` verde no repositório de trabalho (nenhum passo altera `app/` nem `tests/`, então o resultado esperado é sempre `143 passed`).

### Passo 1: validação em máquina limpa (RT-15) — Prompt 42

Roteiro, executado primeiro em PowerShell e depois em Git Bash, cada um no seu diretório (E-02). Cada linha vira uma linha do relatório, com o comando, a saída relevante e "conforme" ou "falha".

| # | PowerShell | Git Bash | Resultado esperado |
| --- | --- | --- | --- |
| 1 | `New-Item -ItemType Directory $env:TEMP\validacao-v100-ps` e entrar nele | `mkdir "$TEMP/validacao-v100-bash"` e entrar nele | diretório vazio fora do repositório |
| 2 | `git clone https://github.com/luisZsiqueira/laboratorio-projeto.git`; `cd laboratorio-projeto` | idem | clone sem erro; `git log -1 --oneline` igual ao `origin/main` do repositório de trabalho |
| 3 | `python -m venv .venv`; `.\.venv\Scripts\Activate.ps1` | `python3 -m venv .venv`; `source .venv/Scripts/activate` (E-03) | `.venv` ativo; `python --version` 3.11 ou superior |
| 4 | `python -m pip install -r requirements.txt` | idem | instalação sem erro; `python -m pip check` responde `No broken requirements found.` |
| 5 | `python -c "import sqlalchemy"` | idem | sem erro; se falhar com `DLL load failed`, Solução de problemas do README na forma do *shell* (E-04, E-05) e repetir |
| 6 | `python -m uvicorn app.main:app --reload`, em segundo plano | idem | log com `Application startup complete.`; `tasks.db` criado na raiz do clone |
| 7 | `Invoke-RestMethod http://127.0.0.1:8000/health` | `curl -i http://127.0.0.1:8000/health` | `200` com `{"status":"ok","database":"ok"}` |
| 8 | exemplos da seção Endpoints, na ordem do README (E-06) | `POST /tasks` (primeiro exemplo) e `GET /tasks` | códigos e forma dos corpos iguais aos do README |
| 9 | parar o servidor | idem | porta 8000 livre |
| 10 | `python -m pytest -W error` | idem | `143 passed`, sem avisos |
| 11 | `git status --porcelain` e `git status --porcelain --ignored` | idem | o primeiro vazio; o segundo só com `.venv/`, `tasks.db`, `.pytest_cache/` e `__pycache__/` |
| 12 | sair do clone e remover `$env:TEMP\validacao-v100-ps` | remover `"$TEMP/validacao-v100-bash"` | diretório removido |

Depois do roteiro: aplicar a E-04 no README do repositório de trabalho; corrigir no README qualquer comando que tenha falhado (E-05 define o que é falha); registrar no relatório o passo 2 do Como rodar em Linux/macOS como não verificado (E-03).

**Arquivos alterados:** `README.md` (Como rodar), `prompts/Prompt 42 - validação em máquina limpa` (registro). **IDs:** RT-15, RNF-01, RNF-02.

### Passo 2: histórico de uso de IA (RT-16) — Prompt 43

Lista de verificação. Cada item vira uma linha do registro do Prompt 43, com o arquivo, a lacuna ("nenhuma" ou a descrição) e o tratamento pela E-08.

1. **Registro da execução em `prompts/`:** todo arquivo `Prompt NN - <título>` tem, depois do separador `---`, o modelo, a data, o resumo e as interações seguintes. Evidência: busca por `Execução:` ou `Modelo:` em cada arquivo. Os Prompts 41 a 43 já devem estar registrados; o 44 é registrado no passo 3.
2. **Entradas do `docs/HISTORY-IA.md`:** uma entrada por arquivo de `prompts/` (00 a 08, 10 a 13, 20 a 43), uma linha por *prompt* na tabela Resumo e uma consolidação por *release* (`v0.1.0` a `v0.5.0`; a da `v1.0.0` é escrita no passo 3).
3. **Numeração:** "Como ler este arquivo" registra que não existem os Prompts 09 e 14 a 19 (E-08, b: o motivo é perguntado ao autor).
4. **Tabela Ambiente:** a linha Modelo cita os modelos de todos os *prompts* (Opus 5.5, Fable 5.1, Sonnet 5.5) até o 43.
5. **README (Uso de IA generativa):** cada assistente e modelo que aparece em `docs/PRE-HISTORY-IA.md`, `docs/EXTRA-HISTORY-IA.md`, `docs/HISTORY-IA.md` e nos registros de `prompts/` está na tabela, com as etapas; a linha da `v1.0.0` é acrescentada; os *links* para os três históricos e para `docs/blueprint-v100.md` estão presentes.
6. **`docs/EXTRA-HISTORY-IA.md`:** *link* do R-01 corrigido (E-09).
7. **`prompts/prompts-desenvolvimento.md`:** linha de status (E-10).
8. **Análise final** (E-11): ganho acumulado somando a coluna "Ganho percebido" do Resumo; horas reais por *release* do `docs/backlog.md`; desafios e decisões humanas tirados das consolidações e das Observações transversais, com a referência ao *prompt* de origem.

**Arquivos alterados:** `docs/HISTORY-IA.md`, `README.md` (Uso de IA generativa), `docs/EXTRA-HISTORY-IA.md` (só o *link*), `prompts/prompts-desenvolvimento.md` (só o status), `prompts/Prompt 43 - consolidação do histórico de uso de IA` (registro). **IDs:** RT-16, RNF-15.

### Passo 3: publicação e fechamento (RT-17) — Prompt 44

Checklist de entrega. Cada item tem evidência (comando e saída, trecho do arquivo ou URL); item não atendido é reportado, nunca omitido.

| # | Requisito do curso (`docs/requerimentos.md`) | Evidência esperada |
| --- | --- | --- |
| 1 | Repositório público, sem informações sensíveis | `curl -s -o /dev/null -w "%{http_code}" https://github.com/luisZsiqueira/laboratorio-projeto` responde `200` sem autenticação; `git ls-files` sem `.env` nem `*.db`; `git log -p --all` sem segredo (mesma busca do Prompt 38) |
| 2 | Histórico de *commits* consistente | `git log --format=%s` com 5 ou mais *commits* no padrão *Conventional Commits* (33 em 07/10/2026) |
| 3 | README: título, descrição, configuração e como rodar | seções Objetivo, Configuração e Como rodar, conferidas no passo 1 |
| 4 | README: exemplos de uso | seção Endpoints, executada no passo 1 |
| 5 | README: tecnologias, modelos de IA e assistentes | seções Stack e Uso de IA generativa, conferidas no passo 2 |
| 6 | README: limitações e próximos passos | seção Limitações e próximos passos |
| 7 | README: créditos e licença | seção Créditos e licença; arquivo `LICENSE` |
| 8 | Gerenciamento de dependências | `requirements.txt`; `pip check` do passo 1 |
| 9 | Testes executáveis e passando | `143 passed` no clone do passo 1 e no clone da *tag* (item 15) |
| 10 | *Release* ou *tag* | itens 13 e 14 |

Depois do checklist, conforme "Fechamento de release" do `CLAUDE.md`:

11. Arquivos: `docs/escopo-mvp.md` (seção 7 toda como atendida, com a evidência, e status do documento); `README.md` por inteiro (E-13, Roadmap, Uso de IA com o Prompt 44); `CHANGELOG.md` (seção `[1.0.0] - 2026-10-dd`, agrupada por tipo de *commit*, e `[Não publicado]` vazio); `docs/backlog.md` (RT-15 a RT-17 concluídos, horas reais da `v1.0.0` pedidas ao autor, totais da tabela Resumo e situação da *release*); `docs/HISTORY-IA.md` (entrada do Prompt 44, consolidação da `v1.0.0`, análise final com as horas totais); status deste *blueprint*; `docs/arquitetura.md` só se o passo 1 mostrar divergência.
12. Depois da autorização do autor: *commits* (E-14), `git switch main`, `git merge --no-ff docs/entrega-v100`, *push* de `main`.
13. `git tag -a v1.0.0 -m "v1.0.0: entrega do curso"` em `main` e `git push origin v1.0.0`. Evidência: URL `https://github.com/luisZsiqueira/laboratorio-projeto/releases/tag/v1.0.0` e `git ls-remote --tags origin v1.0.0`.
14. `gh release create` (E-12). Evidência: URL devolvida pelo comando.
15. Clone da *tag* em `$env:TEMP\validacao-v100-final` (`git clone --branch v1.0.0 ...`), passos 3, 4, 6, 7, 9, 10 e 12 do roteiro do passo 1 em PowerShell (E-01).

**IDs:** RT-17, RNF-13, RNF-14; critérios 2.1 do backlog.

## 5. O que pode e o que não pode mudar

- **Pode:** `README.md`; `CHANGELOG.md`; `docs/escopo-mvp.md` (seção 7 e status); `docs/backlog.md`; `docs/HISTORY-IA.md`; este *blueprint* (status); o *link* de `docs/EXTRA-HISTORY-IA.md` (E-09); o status de `prompts/prompts-desenvolvimento.md` (E-10); o registro de execução nos Prompts 41 a 44; `docs/arquitetura.md` e `CLAUDE.md`, só para corrigir divergência encontrada nos passos.
- **Não pode:** `app/`; `tests/`; `requirements.txt` (E-07); `.gitignore`; `LICENSE`; `docs/decisoes.md`; `docs/requerimentos.md`; `docs/PRE-HISTORY-IA.md`; `docs/release-review-010.md`; `docs/release-prompts-solon-020.md`; *blueprints* anteriores; o texto dos *prompts* (as linhas antes do separador). Nenhum arquivo ou diretório novo além deste *blueprint*; nenhum `Makefile`, `pyproject.toml` ou *script* de validação versionado; nenhuma funcionalidade nova; nenhuma reescrita de histórico publicado.

## 6. Condição de parada

Quem executa para, reporta com a evidência e não improvisa quando:

1. **Um requisito do curso não puder ser marcado como atendido** com evidência (checklist do passo 3). A *tag* e a *Release* não são criadas enquanto houver item pendente; a decisão volta ao autor.
2. Um comando do README falhar (E-05) e a correção exigir mudança fora do README (código, dependência, `.gitignore`).
3. A instalação falhar por versão indisponível ou com conflito (E-07).
4. A definição de pronto falhar ou emitir aviso, no repositório de trabalho ou em qualquer clone.
5. Aparecer segredo real no histórico (reescrever histórico publicado é proibido pelo `CLAUDE.md`).
6. A `gh` não estiver instalada e autenticada no início do Prompt 44 (E-12): pedir ao autor que a instale e rode `! gh auth login`.
7. Uma lacuna do histórico só puder ser preenchida reconstruindo conversa não registrada (E-08).

## 7. Riscos

| Risco | Tratamento |
| --- | --- |
| Smart App Control bloquear o SQLAlchemy no `.venv` novo | E-05; Solução de problemas do README, em PowerShell e em Bash (E-04) |
| Bash não verificável em Linux/macOS nesta máquina | E-03: Git Bash conferido; Linux/macOS registrado como não verificado |
| Porta 8000 ocupada por outra instância da API | passo 1, linha 9: um servidor por vez, parado antes do próximo *shell* |
| Arquivo esquecido no diretório temporário ou no repositório | passo 1, linhas 11 e 12; `git status` no repositório de trabalho ao fim de cada passo |
| Análise final virar texto sem fonte | E-08 e E-11: cada afirmação cita o *prompt* ou o arquivo; estimativas marcadas |
| `gh` ausente bloquear a *Release* | E-12 e condição de parada 6 |
| Publicar com requisito pendente | condição de parada 1: a *tag* é o último passo antes da *Release* |

## 8. Estimativa

| Passo | Item | Horas |
| --- | --- | --- |
| 1 | RT-15 | 0,75 |
| 2 | RT-16 | 0,75 |
| 3 | RT-17 | 0,5 |
| **Itens** | estimativa do backlog | **2** |
| *Blueprint* (este arquivo) e fechamento (passo 3, itens 11 e 15) | fora das estimativas dos itens | 1 |
| **Total da *release*** | | **3** |

Com 19 h reais até a `v0.5.0` e 3 h estimadas para a `v1.0.0`, o projeto fecha em cerca de 22 h, dentro do orçamento de cerca de 30 horas. O tempo da `v0.1.0` não foi medido (`docs/backlog.md`, seção 3).
