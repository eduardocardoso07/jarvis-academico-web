import json

from tools import (
    ferramenta_listar_tarefas,
    ferramenta_adicionar_tarefa,
    ferramenta_concluir_tarefa,
    ferramenta_consultar_agenda_por_periodo,
    ferramenta_consultar_agenda_por_data,
    ferramenta_buscar_material_rag
)


# Função responsável por extrair JSON da resposta da Gemma
def extrair_json_decisao(decisao_gemma):
    texto = decisao_gemma.strip()

    inicio_json = texto.find("{")
    fim_json = texto.rfind("}") + 1

    if inicio_json == -1 or fim_json == 0:
        return None

    texto_json = texto[inicio_json:fim_json]

    try:
        return json.loads(texto_json)
    except json.JSONDecodeError:
        return None


# Função responsável por executar a ferramenta escolhida pela LLM
def executar_ferramenta(decisao_gemma):
    decisao = extrair_json_decisao(decisao_gemma)

    if decisao is None:
        return {
            "tipo_resultado": "resposta_geral",
            "mensagem": "Não consegui identificar uma ferramenta específica para essa mensagem."
        }

    nome_ferramenta = decisao.get("ferramenta")
    parametros = decisao.get("parametros", {})

    if nome_ferramenta == "ferramenta_listar_tarefas":
        return ferramenta_listar_tarefas()

    elif nome_ferramenta == "ferramenta_adicionar_tarefa":
        return ferramenta_adicionar_tarefa(
            parametros.get("descricao", "")
        )

    elif nome_ferramenta == "ferramenta_concluir_tarefa":
        return ferramenta_concluir_tarefa(
            parametros.get("id_tarefa")
        )

    elif nome_ferramenta == "ferramenta_consultar_agenda_por_periodo":
        return ferramenta_consultar_agenda_por_periodo(
            parametros.get("periodo"),
            parametros.get("tipo")
        )

    elif nome_ferramenta == "ferramenta_consultar_agenda_por_data":
        return ferramenta_consultar_agenda_por_data(
            parametros.get("texto_data"),
            parametros.get("tipo")
        )

    elif nome_ferramenta == "ferramenta_buscar_material_rag":
        return ferramenta_buscar_material_rag(
            parametros.get("pergunta", "")
        )

    elif nome_ferramenta == "resposta_geral":
        return {
            "tipo_resultado": "resposta_geral",
            "mensagem": parametros.get("pergunta", "")
        }

    else:
        return {
            "tipo_resultado": "resposta_geral",
            "mensagem": "A mensagem do usuário não exigiu uma ferramenta específica."
        }