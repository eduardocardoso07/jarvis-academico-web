from datetime import date, timedelta


# Função responsável por transformar textos simples em períodos de datas
def resolver_periodo(periodo):
    hoje = date.today()

    if periodo == "hoje":
        inicio = hoje
        final = hoje

    elif periodo == "amanha":
        inicio = hoje + timedelta(days=1)
        final = hoje + timedelta(days=1)

    elif periodo == "essa_semana":
        # Considerando a semana de domingo até sábado
        dias_desde_domingo = (hoje.weekday() + 1) % 7
        inicio = hoje - timedelta(days=dias_desde_domingo)
        final = inicio + timedelta(days=6)

    else:
        return None, None

    return inicio.isoformat(), final.isoformat()

# Função responsável por transformar textos de data específica em uma data real
def resolver_data_especifica(texto_data):
    hoje = date.today()

    # Padroniza o texto recebido
    texto_data = texto_data.lower().strip()

    # Remove acentos simples para facilitar a comparação
    texto_data = texto_data.replace("á", "a")
    texto_data = texto_data.replace("é", "e")
    texto_data = texto_data.replace("í", "i")
    texto_data = texto_data.replace("ó", "o")
    texto_data = texto_data.replace("ú", "u")
    texto_data = texto_data.replace("ç", "c")

    # Troca hífen por espaço
    # Exemplo: "quarta-feira" vira "quarta feira"
    texto_data = texto_data.replace("-", " ")

    # Remove palavras que não mudam a data
    texto_data = texto_data.replace("no ", "")
    texto_data = texto_data.replace("na ", "")
    texto_data = texto_data.replace("que vem", "")
    texto_data = texto_data.replace("proximo ", "")
    texto_data = texto_data.replace("proxima ", "")

    # Remove espaços extras
    texto_data = texto_data.strip()

    # Caso o usuário informe algo como "dia 25"
    if texto_data.startswith("dia "):
        dia_texto = texto_data.replace("dia ", "")
        dia = int(dia_texto)

        data_resolvida = date(hoje.year, hoje.month, dia)

        return data_resolvida.isoformat()

    # Dicionário com os dias da semana
    dias_semana = {
        "segunda": 0,
        "segunda feira": 0,
        "terca": 1,
        "terca feira": 1,
        "quarta": 2,
        "quarta feira": 2,
        "quinta": 3,
        "quinta feira": 3,
        "sexta": 4,
        "sexta feira": 4,
        "sabado": 5,
        "domingo": 6
    }

    # Caso o usuário informe algo como "sabado", "quarta feira" ou "proximo sabado"
    if texto_data in dias_semana:
        dia_semana_desejado = dias_semana[texto_data]
        dia_semana_hoje = hoje.weekday()

        diferenca = dia_semana_desejado - dia_semana_hoje

        # Se o dia já passou ou é hoje, busca a próxima ocorrência desse dia
        if diferenca <= 0:
            diferenca = diferenca + 7

        data_resolvida = hoje + timedelta(days=diferenca)

        return data_resolvida.isoformat()

    return None