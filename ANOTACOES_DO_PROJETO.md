# Anotações do Projeto — JARVIS Acadêmico

## Funcionalidade 3.3 — Lista de tarefas

Esta funcionalidade permite que o usuário controle tarefas acadêmicas.

Até agora o sistema consegue:

- adicionar uma nova tarefa;
- listar todas as tarefas;
- marcar uma tarefa como concluída;
- salvar as tarefas no arquivo `data/tarefas.json`.

## Arquivo `src/tarefas.py`

Este arquivo concentra as funções relacionadas às tarefas.

Funções criadas:

- `carregar_tarefas()`: carrega as tarefas salvas no JSON.
- `salvar_tarefas(tarefas)`: salva a lista de tarefas no JSON.
- `adicionar_tarefa(descricao)`: cria uma nova tarefa pendente.
- `listar_tarefas()`: retorna todas as tarefas cadastradas.
- `concluir_tarefa(id_tarefa)`: marca uma tarefa como concluída.

## Funcionalidade 3.2 — Agenda acadêmica

Esta funcionalidade permite consultar eventos acadêmicos salvos em um arquivo JSON.

Até agora o sistema consegue:

- carregar eventos do arquivo `data/agenda.json`;
- listar todos os eventos;
- buscar eventos por uma data específica;
- buscar eventos por um período;
- interpretar períodos simples como `hoje`, `amanha` e `essa_semana`.

## Arquivo `src/agenda.py`

Este arquivo concentra as funções relacionadas à agenda acadêmica.

Funções criadas:

- `carregar_agenda()`: carrega os eventos salvos no JSON.
- `listar_eventos()`: retorna todos os eventos cadastrados.
- `buscar_eventos_por_data(data_buscada)`: retorna eventos de uma data específica.
- `buscar_eventos_por_periodo(inicio, final)`: retorna eventos dentro de um intervalo de datas.
- `filtrar_eventos_por_tipo(eventos, tipo)`: filtra uma lista de eventos pelo tipo, como `aula`, `prova` ou `trabalho`.

## Arquivo `src/datas.py`

Este arquivo concentra funções auxiliares relacionadas a datas.

Funções criadas:

- `resolver_periodo(periodo)`: transforma textos simples como `hoje`, `amanha` e `essa_semana` em datas no formato `yyyy-mm-dd`.

---

# Arquivo `src/tools.py`

Este arquivo funciona como uma ponte entre a LLM Gemma 12B e as funções internas do sistema.

A ideia é que a LLM não acesse diretamente os arquivos `agenda.py`, `tarefas.py` ou `datas.py`.

Em vez disso, ela deve chamar ferramentas organizadas no arquivo `tools.py`.

## Ferramentas de tarefas

- `ferramenta_listar_tarefas()`: retorna todas as tarefas cadastradas.
- `ferramenta_adicionar_tarefa(descricao)`: adiciona uma nova tarefa.
- `ferramenta_concluir_tarefa(id_tarefa)`: marca uma tarefa como concluída.

## Ferramentas de agenda

- `ferramenta_consultar_agenda_por_periodo(periodo, tipo=None)`: consulta eventos por período, como `hoje`, `amanha` ou `essa_semana`. O parâmetro `tipo` é opcional.

- `ferramenta_consultar_agenda_por_data(texto_data, tipo=None)`: consulta eventos por data específica, como `dia 25`, `sabado` ou `proxima quarta`. O parâmetro `tipo` é opcional.

## Exemplos de uso

Pergunta do usuário:

`Tenho algo essa semana?`

Chamada esperada:

`ferramenta_consultar_agenda_por_periodo("essa_semana")`

Pergunta do usuário:

`Tenho prova essa semana?`

Chamada esperada:

`ferramenta_consultar_agenda_por_periodo("essa_semana", "prova")`

Pergunta do usuário:

`Tenho aula no dia 25?`

Chamada esperada:

`ferramenta_consultar_agenda_por_data("dia 25", "aula")`

## Decisão de projeto

Foi decidido usar ferramentas com parâmetros opcionais em vez de criar uma ferramenta separada para cada combinação.

Isso deixa o projeto mais simples, evita repetição de código e facilita a integração com a LLM.

A LLM será responsável por interpretar a frase do usuário e enviar apenas os parâmetros necessários para a ferramenta.

O Python será responsável por executar a lógica de forma segura.

---

# Arquivo `src/logger.py`

Este arquivo é responsável por registrar o uso das ferramentas do sistema.

O enunciado do trabalho exige que o sistema registre logs com:

- ferramenta chamada;
- entrada recebida;
- saída retornada.

Para isso, foi criada a função `registrar_log()`.

## Função criada

- `registrar_log(nome_ferramenta, entrada, saida)`: salva no arquivo `data/logs.json` as informações sobre o uso de uma ferramenta.

## Exemplo de log

```json
{
    "data_hora": "2026-05-24T10:30:00",
    "ferramenta": "ferramenta_listar_tarefas",
    "entrada": {},
    "saida": [
        {
            "id": 1,
            "descricao": "Estudar embeddings para a prova de IA",
            "concluida": false
        }
    ]
}

---

# Integração com a LLM Gemma 12B

O sistema foi integrado com a LLM obrigatória do trabalho, a Gemma 12B.

A conexão com a LLM foi feita no arquivo `src/gemma.py`, usando o endpoint fornecido no enunciado do trabalho.

## Arquivo `src/gemma.py`

Este arquivo é responsável pela comunicação com a Gemma 12B.

Funções criadas:

- `perguntar_llm(pergunta)`: envia uma pergunta simples para a LLM e retorna a resposta.
- `decidir_ferramenta(pergunta_usuario)`: envia a pergunta do usuário para a LLM e pede que ela escolha qual ferramenta deve ser chamada.

## Decisão de projeto

A Gemma não executa diretamente as funções do sistema.

Ela apenas interpreta a pergunta do usuário e retorna uma decisão em formato JSON.

Exemplo:

```json
{
    "ferramenta": "ferramenta_consultar_agenda_por_periodo",
    "parametros": {
        "periodo": "essa_semana",
        "tipo": "prova"
    }
}