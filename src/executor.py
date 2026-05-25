import json
from tools import ferramenta_listar_tarefas, ferramenta_adicionar_tarefa, ferramenta_concluir_tarefa, ferramenta_consultar_agenda_por_periodo, ferramenta_consultar_agenda_por_data, ferramenta_buscar_material_rag



# Função responsável por executar a ferramenta escolhida pela LLM
def executar_ferramenta(decisao_gemma):
    # Limpa a resposta da LLM e tenta extrair apenas o JSON
    texto = decisao_gemma.strip()

    inicio_json = texto.find("{")
    fim_json = texto.rfind("}") + 1

    texto_json = texto[inicio_json:fim_json]

    # Converte a resposta da LLM, que vem em texto JSON, para dicionário Python
    decisao = json.loads(texto_json)

    nome_ferramenta = decisao["ferramenta"]
    parametros = decisao.get("parametros", {})

    if nome_ferramenta == "ferramenta_listar_tarefas":
        return ferramenta_listar_tarefas()

    elif nome_ferramenta == "ferramenta_adicionar_tarefa":
        return ferramenta_adicionar_tarefa(parametros["descricao"])

    elif nome_ferramenta == "ferramenta_concluir_tarefa":
        return ferramenta_concluir_tarefa(int(parametros["id_tarefa"]))

    elif nome_ferramenta == "ferramenta_consultar_agenda_por_periodo":
        return ferramenta_consultar_agenda_por_periodo(parametros["periodo"],parametros.get("tipo"))

    elif nome_ferramenta == "ferramenta_consultar_agenda_por_data":
        return ferramenta_consultar_agenda_por_data(parametros["texto_data"], parametros.get("tipo"))
    
    elif nome_ferramenta == "ferramenta_buscar_material_rag":
        return ferramenta_buscar_material_rag(parametros["pergunta"])

    else:
        return {
            "erro": "Ferramenta não reconhecida."
        }