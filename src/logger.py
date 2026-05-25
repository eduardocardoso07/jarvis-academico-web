import json
from datetime import datetime


# Caminho do arquivo onde os logs serão salvos
CAMINHO_LOGS = "data/logs.json"


# Função responsável por registrar o uso de uma ferramenta
def registrar_log(nome_ferramenta, entrada, saida):
    log = {
        "data_hora": datetime.now().isoformat(),
        "ferramenta": nome_ferramenta,
        "entrada": entrada,
        "saida": saida
    }

    try:
        with open(CAMINHO_LOGS, "r", encoding="utf-8") as arquivo:
            logs = json.load(arquivo)
    except FileNotFoundError:
        logs = []

    logs.append(log)

    with open(CAMINHO_LOGS, "w", encoding="utf-8") as arquivo:
        json.dump(logs, arquivo, indent=4, ensure_ascii=False)