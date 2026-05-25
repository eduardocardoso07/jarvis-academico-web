from tarefas import adicionar_tarefa, listar_tarefas, concluir_tarefa
from agenda import buscar_eventos_por_data, buscar_eventos_por_periodo, filtrar_eventos_por_tipo
from datas import resolver_periodo, resolver_data_especifica
from logger import registrar_log
from rag import carregar_documentos, dividir_em_chunks, gerar_embeddings_chunks, buscar_chunks_por_embedding, gerar_resposta_rag

# Ferramenta responsável por listar todas as tarefas cadastradas
def ferramenta_listar_tarefas():
    entrada = {}

    tarefas = listar_tarefas()

    registrar_log(
        nome_ferramenta="ferramenta_listar_tarefas",
        entrada=entrada,
        saida=tarefas
    )

    return tarefas

# Ferramenta responsável por adicionar uma nova tarefa
def ferramenta_adicionar_tarefa(descricao):
    entrada = {
        "descricao": descricao
    }

    tarefa = adicionar_tarefa(descricao)

    registrar_log(
        nome_ferramenta="ferramenta_adicionar_tarefa",
        entrada=entrada,
        saida=tarefa
    )

    return tarefa

# Ferramenta responsável por concluir uma tarefa pelo ID
def ferramenta_concluir_tarefa(id_tarefa):
    entrada = {
        "id_tarefa": id_tarefa
    }

    # Tenta converter o ID recebido para número inteiro
    try:
        id_tarefa_convertido = int(id_tarefa)

    except ValueError:
        # Se a Gemma mandar algo como "essa", "ela" ou outro texto,
        # o sistema tenta identificar se existe apenas uma tarefa pendente.
        tarefas = listar_tarefas()

        tarefas_pendentes = []

        for tarefa in tarefas:
            if tarefa["concluida"] == False:
                tarefas_pendentes.append(tarefa)

        # Se existir apenas uma tarefa pendente, o sistema conclui essa tarefa
        if len(tarefas_pendentes) == 1:
            id_tarefa_convertido = tarefas_pendentes[0]["id"]

        else:
            saida = {
                "erro": "Não consegui identificar qual tarefa deve ser concluída. Informe o ID da tarefa."
            }

            registrar_log(
                nome_ferramenta="ferramenta_concluir_tarefa",
                entrada=entrada,
                saida=saida
            )

            return saida

    tarefa = concluir_tarefa(id_tarefa_convertido)

    registrar_log(
        nome_ferramenta="ferramenta_concluir_tarefa",
        entrada=entrada,
        saida=tarefa
    )

    return tarefa

# Ferramenta responsável por consultar eventos da agenda por período
def ferramenta_consultar_agenda_por_periodo(periodo, tipo=None):
    entrada = {
        "periodo": periodo,
        "tipo": tipo
    }

    inicio, final = resolver_periodo(periodo)

    if inicio is None or final is None:
        eventos = []
    else:
        eventos = buscar_eventos_por_periodo(inicio, final)

        if tipo is not None:
            eventos = filtrar_eventos_por_tipo(eventos, tipo)

    registrar_log(
        nome_ferramenta="ferramenta_consultar_agenda_por_periodo",
        entrada=entrada,
        saida=eventos
    )

    return eventos

# Ferramenta responsável por consultar eventos da agenda por data específica
def ferramenta_consultar_agenda_por_data(texto_data, tipo=None):
    entrada = {
        "texto_data": texto_data,
        "tipo": tipo
    }

    data_resolvida = resolver_data_especifica(texto_data)

    if data_resolvida is None:
        eventos = []
    else:
        eventos = buscar_eventos_por_data(data_resolvida)

        if tipo is not None:
            eventos = filtrar_eventos_por_tipo(eventos, tipo)

    registrar_log(
        nome_ferramenta="ferramenta_consultar_agenda_por_data",
        entrada=entrada,
        saida=eventos
    )

    return eventos

# Ferramenta responsável por consultar os materiais nos documentos usando RAG
def ferramenta_buscar_material_rag(pergunta):
    entrada = {
        "pergunta": pergunta
    }

    documentos = carregar_documentos()
    chunks = dividir_em_chunks(documentos)
    chunks = gerar_embeddings_chunks(chunks)
    chunks_relevantes = buscar_chunks_por_embedding(pergunta, chunks)
    resposta = gerar_resposta_rag(pergunta, chunks_relevantes)

    saida = {
        "resposta": resposta,
        "chunks_usados": [
            {
                "documento": chunk["documento"],
                "conteudo": chunk["conteudo"],
                "similaridade": float(chunk["similaridade"])
            }
            for chunk in chunks_relevantes
        ]
    }

    registrar_log(
        nome_ferramenta="ferramenta_buscar_material_rag",
        entrada=entrada,
        saida=saida
    )

    return saida