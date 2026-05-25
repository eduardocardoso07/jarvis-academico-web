import json
import os
from datetime import date

# Caminho do arquivo onde os eventos da agenda estão salvos
CAMINHO_AGENDA = "data/agenda.json"


# Função responsável por carregar os eventos da agenda
def carregar_agenda():
    if not os.path.exists(CAMINHO_AGENDA):
        return []

    with open(CAMINHO_AGENDA, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
    

# Função responsável por listar todos os eventos da agenda
def listar_eventos():
    eventos = carregar_agenda()
    return eventos

# Função responsável por buscar os eventos por data
def buscar_eventos_por_data(data_buscada):
    eventos = carregar_agenda()

    eventos_buscados = []
    
    for evento in eventos:
        if evento["data"] == data_buscada:
            eventos_buscados.append(evento)

    return eventos_buscados

# Função responsável por buscar os eventos por período
def buscar_eventos_por_periodo(inicio, final):
    eventos = carregar_agenda()

    eventos_buscados = []

    for evento in eventos:
        if (evento["data"] >= inicio) and (evento["data"] <= final):
            eventos_buscados.append(evento)

    return eventos_buscados

# Função responsável por filtrar eventos pelo tipo
def filtrar_eventos_por_tipo(eventos, tipo):
    eventos_filtrados = []

    for evento in eventos:
        if evento["tipo"] == tipo:
            eventos_filtrados.append(evento)

    return eventos_filtrados

