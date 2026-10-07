# Blueprint da `v0.5.0`: revisão

> **Status:** proposto em 06/10/2026 (Prompt 36) e aprovado pelo autor no mesmo dia. Execução prevista: Prompt 37 (passo 1), Prompt 38 (passo 2), Prompt 39 (passos 3 e 4) e Prompt 40 (passo 5, fechamento). Quem executa lê este arquivo e o `CLAUDE.md`; nada depende do histórico do *chat*.

## 1. Escopo da *release*

Revisão do que existe, sem funcionalidade nova. Os critérios de aceite são os de `docs/backlog.md` (seção 4.4), copiados abaixo, mais os critérios comuns do backlog (seção 2).

| Passo | ID | Revisão | Critérios de aceite (backlog) | Prompt |
| --- | --- | --- | --- | --- |
| 1 | RT-11 | Arquitetura | 1. Importações conferidas contra o diagrama de módulos de `docs/arquitetura.md`; nenhuma dependência para cima **[I]**<br>2. Divergências corrigidas no código ou registradas em `docs/arquitetura.md` (ajuste pontual ou novo ADR) **[I]** | 37 |
| 2 | RT-12 | Segurança | 1. Nenhum SQL montado por concatenação ou *f-string* **[I]**<br>2. Respostas de erro (404, 422, 500, 503) sem detalhes internos **[T]**<br>3. Varredura de segredos no repositório e no histórico **[C]**<br>4. Documentação desabilitada em produção confirmada **[T]** | 38 |
| 3 | RT-14 | Dependências (roteiro de APIs deprecadas) | 1. Versões do `requirements.txt` conferidas com o PyPI, com data **[C]**<br>2. Se alguma versão mudar: notas de versão lidas, testes mínimos executados e tabela do `CLAUDE.md` atualizada **[C]**<br>3. `python -m pip check` sem conflitos **[C]** | 39 |
| 4 | RT-13 | Documentação | 1. README conferido contra o comportamento real da API: endpoints, códigos e exemplos executados **[C]**<br>2. *Docstrings* presentes em todas as classes e funções públicas **[I]**<br>3. `docs/escopo-mvp.md` sem decisões em aberto pendentes **[I]** | 39 |
| 5 | — | Fechamento | `CLAUDE.md`, Fechamento de release | 40 |

**Ordem e motivo.** Arquitetura e segurança primeiro, porque são as únicas que podem mudar código. Depois, dependências, porque uma versão nova mudaria o código ou o README (Stack). A documentação vem por último, para ser conferida contra o código e as versões finais. No Prompt 39, as dependências (passo 3) vêm antes da documentação (passo 4).

## 2. Decisões tomadas

Não há decisão em aberto. As decisões abaixo são confirmadas na aprovação.

| ID | Decisão | Motivo |
| --- | --- | --- |
| R-01 | Regra de decisão entre código e documento: ver seção 4 | evita refatoração além dos desvios |
| R-02 | Critério de promoção de DT a ADR: ver seção 5, já aplicado às DT-01 a DT-15 | a revisão da `v0.5.0` é o ponto previsto no `CLAUDE.md` (Decisões técnicas) |
| R-03 | Novo ADR-19, composição da aplicação: `create_app(settings, db_engine)` cria a aplicação e grava as `Settings` em `application.state.settings`, de onde as rotas as leem (promove DT-01 e DT-15) | afeta a dependência entre `main.py`, rotas e configurações |
| R-04 | Novo ADR-20, conversão de formato em `app/models/`: os modelos podem conter conversão de tipo e de formato sem regra de negócio (`UTCDateTime`, `convert_priority_text`, `parse_local_due_at`); regra de negócio continua só em `app/services/` (promove DT-04, DT-12 e DT-13; ajusta a frase "sem lógica" do ADR-01) | o diagrama e o `CLAUDE.md` dizem "modelos sem lógica", e o código tem essas três conversões; movê-las para o *service* tiraria a validação de formato dos esquemas e mudaria o `422` |
| R-05 | O `loc` do `422` de formato de `due_at` com o nome `parse_local_due_at` não é tratado como detalhe interno proibido: a seção Segurança do `CLAUDE.md` proíbe *stack trace*, SQL e caminhos; o nome do validador não revela nenhum dos três. Fica como está, documentado nas Limitações do README | mudar exigiria um tradutor próprio de erros de validação, ou seja, mudança de contrato do `422` (ADR-15) |
| R-06 | Versões das dependências: nenhuma atualização na `v0.5.0`, salvo vulnerabilidade publicada ou correção de defeito que afete o projeto. Versão mais nova sem esses motivos é registrada como "disponível, não adotada" | estabilidade antes da entrega; o `CLAUDE.md` exige justificativa e fonte para mudar versão |
| R-07 | O checklist de cada revisão fica no registro do arquivo do *prompt* (`prompts/Prompt 37` a `39`) e é resumido em `docs/HISTORY-IA.md`. Nenhum arquivo novo | a estrutura de diretórios é fechada |

## 3. Forma do checklist

Uma tabela por revisão, uma linha por verificação, inclusive as que não acham desvio:

| # | Arquivo e linha | Regra conferida (fonte) | Desvio | Evidência | Ação |
| --- | --- | --- | --- | --- | --- |
| 1 | `app/api/task_routes.py:15` | rotas sem acesso ao banco (`CLAUDE.md`, ADR-01) | nenhum | `grep -n "^from\|^import" app/api/task_routes.py`: importa `get_db` só para `Depends` | sem ação |

- **Arquivo e linha:** caminho relativo à raiz e número da linha; "todos" quando a verificação é global.
- **Regra conferida:** a regra e onde ela está escrita (`CLAUDE.md`, ADR, DT, RNF).
- **Desvio:** "nenhum" ou o desvio em uma frase.
- **Evidência:** o comando executado e o resultado, ou o trecho lido.
- **Ação:** "sem ação", "corrigido" (com o arquivo alterado) ou "registrado em" (com o documento e a seção).

## 4. Regra de decisão: corrigir no código ou registrar em documento

1. **Corrigir no código** quando o desvio contraria uma regra escrita (`CLAUDE.md`, ADR ou DT), a correção é local e os testes existentes continuam passando sem mudar o comportamento da API.
2. **Corrigir no código, mesmo mudando comportamento,** quando o desvio expõe detalhe interno proibido pela seção Segurança do `CLAUDE.md` (*stack trace*, SQL, caminho, segredo). A correção vem com teste em `tests/test_task_routes.py` e com a mudança registrada no `CHANGELOG.md`.
3. **Registrar em documento** quando o código reflete uma escolha consciente que diverge de uma regra genérica: novo ADR ou ajuste pontual em `docs/arquitetura.md` (seção 6) e, se a regra estiver no `CLAUDE.md`, a correção do `CLAUDE.md` no fechamento (passo 5).
4. **Registrar como limitação** (README, Limitações) quando corrigir exigiria funcionalidade nova, dependência nova ou mudança de contrato sem motivo de segurança.
5. Em qualquer outro caso, parar e reportar (seção 8).

## 5. Promoção de DT a ADR

**Critério:** a DT vira ADR quando afeta camadas, dependência entre módulos, persistência ou contrato da API (`CLAUDE.md`, Decisões técnicas) **e** nenhum ADR existente já a declara. Se um ADR já a declara, a DT fica e o ADR passa a citá-la. A DT promovida continua em `docs/decisoes.md`, com a linha "Promovida ao ADR-NN".

Aplicação às DTs existentes (o passo 1 confirma; só muda se o código contrariar esta tabela):

| DT | Afeta | ADR que já a declara | Resultado |
| --- | --- | --- | --- |
| DT-01, DT-15 | dependência entre `main.py`, rotas e configurações | nenhum | **promovidas ao ADR-19** |
| DT-04, DT-12, DT-13 | camada de modelos (conversões) | ADR-10 e ADR-18 em parte; nenhum declara a exceção a "modelos sem lógica" | **promovidas ao ADR-20** |
| DT-05 | contrato (`PATCH` recusa `null`) | nenhum | ADR-15 passa a citá-la (detalhe do contrato já registrado) |
| DT-11 | camadas (resposta montada no *service*) | ADR-16 e ADR-17 em parte | ADR-17 passa a citá-la |
| DT-14 | configuração | ADR-18 | ADR-18 já a cita; sem ação |
| DT-10 | regra de negócio no *service* | ADR-17 (contrato do `422`) | sem ação |
| DT-02, DT-03, DT-06 a DT-09 | local ao código ou aos testes | — | permanecem DT |

## 6. Passos

Cada passo termina com a definição de pronto verde, na raiz, com o `.venv` ativo: `python -m pytest -W error`. Estado inicial: 134 testes, mypy sem erros em 18 arquivos. A partir do passo 2 (Prompt 38, 07/10/2026), o mypy deixou de ser usado (ADR-21): sai da definição de pronto e do `requirements.txt`.

### Passo 1: arquitetura (RT-11) — Prompt 37

Verificações, cada uma uma linha do checklist:

1. Cada `import` de `app/` contra o diagrama de módulos (`docs/arquitetura.md`, seção 2): rotas sem *repository* e sem consulta (só `get_db` em `Depends`); *services* sem FastAPI e Starlette; *repositories* sem *services*; *models* sem *services*, *repositories* e `api`; `main.py` só composição. Evidência: `grep -rn "^from\|^import" app`.
2. Funções com mais de uma responsabilidade ou acima de cerca de 30 linhas. Evidência: contagem por `ast` (na proposta, nenhuma função de `app/` passa de 20 linhas de código).
3. Conjuntos fechados sem `typing.Literal`.
4. Nomes fora da nomenclatura semântica (`CLAUDE.md`, Convenções de código).
5. Aplicação da seção 5: ADR-19 e ADR-20 em `docs/arquitetura.md` (seção 6); citações no ADR-15 e no ADR-17; linha "Promovida ao ADR-NN" nas DT-01, DT-04, DT-12, DT-13 e DT-15; frase "Models … sem lógica" da tabela da seção 1 e do subgrafo do diagrama de módulos ajustada ao ADR-20, com antes e depois em `docs/mermaid.md`.

**IDs:** RT-11, RNF-05, RNF-06, ADR-01.

### Passo 2: segurança (RT-12) — Prompt 38

1. SQL: `grep -rn "text(\|execute(\|f\"\|f'\|%s\|\.format(" app`. Esperado: só `text("SELECT 1")` em `database.py`, sem parâmetro externo, e *f-strings* apenas em mensagens de exceção de domínio.
2. Entrada: todo parâmetro de rota, de consulta e corpo tipado por esquema Pydantic ou `Literal` (`task_id: int`, `TaskStatus`, `TaskPriorityQuery`, esquemas de corpo).
3. Respostas de erro sem detalhe interno, conferidas pelos testes existentes: `test_task_routes_return_404_for_missing_task`, `test_create_task_rejects_priority_four_without_due_at_with_422`, `test_database_failure_returns_500_without_internal_details`, `test_health_returns_503_without_internal_details_when_database_fails`. Lacuna encontrada vira teste novo em `tests/test_task_routes.py`, nomeado `test_<cenário>_has_no_internal_details`. O `422` de formato segue a R-05.
4. Documentação em produção: `test_docs_disabled_in_production`.
5. Segredos: `git ls-files | grep -i "\.env"` (esperado: nada); `git log -p --all | grep -inE "api[_-]?key|secret|token|password|senha|BEGIN .*PRIVATE"` com cada ocorrência classificada (texto de documentação ou segredo); `git check-ignore .env tasks.db`.
6. Logs: as chamadas `logger.*` de `app/` não registram corpo de requisição nem configuração.

**IDs:** RT-12, RNF-08, RNF-09, RNF-10.

### Passo 3: dependências (RT-14) — Prompt 39

1. Para cada pacote direto do `requirements.txt` (`fastapi`, `uvicorn`, `SQLAlchemy`, `pydantic`, `pydantic-settings`, `pytest`, `httpx2`; o `mypy` saiu pelo ADR-21), consultar o PyPI e registrar: versão fixada, última versão, data da consulta e decisão pela R-06.
2. `python -m pip check` (esperado: "No broken requirements found.").
3. Se uma versão mudar pela R-06: notas de versão lidas, testes mínimos do roteiro (`CLAUDE.md`, APIs deprecadas) executados com `-W error`, tabela do roteiro, `requirements.txt` e README (Stack) atualizados. Sem mudança, a tabela do roteiro não muda.

**IDs:** RT-14, RNF-02, RNF-04.

### Passo 4: documentação (RT-13) — Prompt 39

1. Subir a API com banco temporário fora do repositório, sem `--reload` (como no Prompt 34), e executar todos os exemplos da seção Endpoints do README em PowerShell, na ordem do README. Divergência de código ou de corpo é corrigida no README. Os instantes, os `id` e a `suggested_priority` mudam com a execução e não contam como divergência.
2. Configuração e Como rodar conferidos em PowerShell.
3. *Docstrings*: toda classe e função pública de `app/` tem *docstring* (contagem por `ast`).
4. `docs/escopo-mvp.md` sem decisão em aberto; `docs/arquitetura.md` e `docs/mermaid.md` coerentes com o código depois do passo 1.

**IDs:** RT-13, RNF-13.

### Passo 5: fechamento — Prompt 40

Conforme "Fechamento de release" do `CLAUDE.md`: README por inteiro; `docs/arquitetura.md` com os ADR-19 e ADR-20; `docs/backlog.md` com RT-11 a RT-14 concluídos e horas reais pedidas ao autor; `CHANGELOG.md` com a seção `0.5.0`; `docs/HISTORY-IA.md` com os Prompts 36 a 40, os checklists resumidos e a consolidação; `CLAUDE.md` corrigido no que a revisão mostrou divergente (no mínimo, a frase "`app/models/`: … sem lógica", ajustada ao ADR-20); status deste *blueprint*. Depois da aprovação: *commits*, *merge* `--no-ff`, *tag* anotada `v0.5.0`, *push* e definição de pronto em clone limpo.

## 7. O que pode e o que não pode mudar

- **Pode:** correções locais de código que eliminem desvios (seção 4, itens 1 e 2); testes novos em `tests/test_task_routes.py` para lacunas de segurança; *docstrings* faltantes; documentação (`README.md`, `docs/`, `CLAUDE.md`).
- **Não pode:** funcionalidade nova; dependência nova ou versão nova sem a R-06; arquivo ou diretório novo (além deste *blueprint*); arquivo de teste novo; alteração da tabela `tasks`; mudança de contrato da API sem motivo de segurança; alteração de testes existentes, salvo para acompanhar uma correção de segurança; refatoração além dos desvios encontrados; `docs/requerimentos.md`, `docs/PRE-HISTORY-IA.md`, `docs/EXTRA-HISTORY-IA.md`, `docs/release-review-010.md`, `docs/release-prompts-solon-020.md`, *blueprints* anteriores, `LICENSE` e `.gitignore`.

## 8. Condição de parada

Se uma verificação achar desvio que a seção 4 não resolve, se um segredo real aparecer no histórico (reescrever histórico publicado é proibido pelo `CLAUDE.md`) ou se a definição de pronto falhar de forma não prevista, quem executa para, reporta com a evidência e não improvisa.

## 9. Riscos

| Risco | Tratamento |
| --- | --- |
| Revisão virar refatoração | seção 4 e seção 7; checklist com uma linha por verificação |
| Correção quebrar comportamento | definição de pronto a cada passo; testes existentes inalterados, salvo correção de segurança |
| Atualização de dependência introduzir aviso | R-06 (sem atualização sem motivo); roteiro de checagem se houver mudança |
| Exemplos do README divergirem por depender do instante | só código e forma do corpo contam como divergência (passo 4) |
| Segredo encontrado no histórico | condição de parada; a decisão (rotação do segredo e registro) fica com o autor |

## 10. Estimativa

| Passo | Item | Horas |
| --- | --- | --- |
| 1 | RT-11 | 0,5 |
| 2 | RT-12 | 1 |
| 3 | RT-14 | 0,5 |
| 4 | RT-13 | 0,5 |
| **Itens** | estimativa do backlog | **2,5** |
| *Blueprint* (este arquivo) e fechamento (passo 5) | fora das estimativas dos itens | 1,5 |
| **Total da *release*** | | **4** |

Com 15 h reais até a `v0.4.0`, 4 h da `v0.5.0` e 3 h da `v1.0.0` (2 h dos itens, mais *blueprint* e fechamento), a projeção do projeto fica em cerca de 22 h, dentro do orçamento de cerca de 30 horas.
