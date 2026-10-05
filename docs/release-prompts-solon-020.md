# Definições mínimas

<!-- Print 1 — legenda informada: "Prompt 21 - Modelo Pydantic" -->
## Prompt 21 - Modelo Pydantic

```text
Contexto: API de tarefas em FastAPI para uso interno de equipe.
Objetivo: Gerar modelos TaskCreate, TaskUpdate e TaskOut com tipagem e validacoes.
Estilo: Pydantic v2, codigo limpo e docstrings curtas.
Resposta: Apenas codigo de app/models/task.py.
```

<!-- Print 2 — legenda informada: "Prompt 22 - Repositorio inicial" -->
<!-- Alteração solicitada pelo usuário: "primeira release" → "esta release" -->
## Prompt 22 - Repositorio inicial

```text
Contexto: Preciso de persistencia inicial enxuta para viabilizar esta release.
Objetivo: Criar TaskRepository em memoria com create, list, get_by_id, update e delete.
Estilo: Python tipado, sem dependencias externas.
Resposta: Codigo completo de app/repositories/task_repository.py.
```

<!-- Print 3 — legenda informada: "Prompt 23 - Service com regra de prioridade" -->
## Prompt 23 - Service com regra de prioridade

```text
Contexto: A prioridade da tarefa pode ser sugerida automaticamente.
Objetivo: Criar TaskService que use TaskRepository e PriorityAdvisor.
Estilo: Separar regra de negocio da camada de API.
Resposta: Codigo de app/services/task_service.py.
```

<!-- Print 4 — legenda informada: "Prompt 24 - PriorityAdvisor com fallback" -->
<!-- Objetivo unido em uma linha (quebra visual do editor no print) -->
## Prompt 24 - PriorityAdvisor com fallback

```text
Contexto: Quero rodar sem custo de API quando nao houver chave.
Objetivo: Implementar PriorityAdvisor com heuristica local e chamada opcional a LLM quando OPENAI_API_KEY existir.
Estilo: Falha segura, timeout e fallback obrigatorio.
Resposta: Codigo de app/services/priority_advisor.py.
```

<!-- Print 5 — legenda informada: "Prompt 25 - Rotas CRUD" -->
<!-- Objetivo unido em uma linha (quebra visual do editor no print) -->
## Prompt 25 - Rotas CRUD

```text
Contexto: FastAPI com TaskService pronto.
Objetivo: Criar rotas POST/GET/PUT/DELETE para tarefas com status HTTP corretos e tratamento de 404.
Estilo: Router separado em app/api/task_routes.py.
Resposta: Apenas o codigo do arquivo.
```

<!-- Print 6 — legenda informada: "Prompt 26 - Revisao tecnica" -->
## Prompt 26 - Revisao tecnica

```text
Revise os arquivos do core da API e responda:
1) Quais pontos de acoplamento estao altos?
2) Onde faltam validacoes?
3) Quais 5 testes devo priorizar na proxima release?
Resposta em checklist.
```
