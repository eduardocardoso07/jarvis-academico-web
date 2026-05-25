import json
import os

# Caminho do arquivo onde está salvo as tarefas
CAMINHO_TAREFAS = "data/tarefas.json"

# Função responsável por carregar as tarefas do arquivo JSON
def carregar_tarefas():
    if not os.path.exists(CAMINHO_TAREFAS):
        return []

    with open(CAMINHO_TAREFAS, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

# Função responsável por salvar a lista de tarefas no arquivo JSON
def salvar_tarefas(tarefas):
    with open(CAMINHO_TAREFAS, "w", encoding="utf-8") as arquivo:
        json.dump(tarefas, arquivo, indent=4, ensure_ascii=False)


# Função responsável por adicionar uma nova tarefa
def adicionar_tarefa(descricao):
    tarefas = carregar_tarefas()

    nova_tarefa = {
        "id": len(tarefas) + 1,
        "descricao": descricao,
        "concluida": False
    }

    tarefas.append(nova_tarefa)
    salvar_tarefas(tarefas)

    return nova_tarefa

# Função responsável por marcar uma tarefa como concluída
def concluir_tarefa(id_tarefa):
    tarefas = carregar_tarefas()

    for tarefa in tarefas:
        if tarefa["id"] == id_tarefa:
            tarefa["concluida"] = True
            salvar_tarefas(tarefas)
            return tarefa

    return None

# Função responsável por listar todas as tarefas que estão cadastradas
def listar_tarefas():
    tarefas = carregar_tarefas()
    return tarefas 

