import os
from openai import OpenAI
from dotenv import load_dotenv


# Carrega as variáveis salvas no arquivo .env
load_dotenv()


# Cliente responsável por se conectar com a LLM Gemma 12B
client = OpenAI(
    base_url="https://llm.liaufms.org/v1/gemma-3-12b-it",
    api_key=os.getenv("GEMMA_API_KEY")
)


# Função responsável por enviar uma pergunta simples para a LLM
def perguntar_llm(pergunta):
    resposta = client.chat.completions.create(
        model="google/gemma-3-12b-it",
        messages=[
            {
                "role": "user",
                "content": pergunta
            }
        ]
    )

    return resposta.choices[0].message.content


# Função responsável por pedir para a LLM decidir qual ferramenta deve ser chamada
def decidir_ferramenta(pergunta_usuario):
    prompt = f"""
Você é o JARVIS Acadêmico, um assistente para estudantes.

Sua tarefa é analisar a pergunta do usuário e decidir qual ferramenta do sistema deve ser chamada.

Ferramentas disponíveis:

1. ferramenta_listar_tarefas
Use quando o usuário quiser ver/listar suas tarefas.
Não precisa de parâmetros.

2. ferramenta_adicionar_tarefa
Use quando o usuário quiser adicionar uma nova tarefa.
Parâmetro necessário:
- descricao

3. ferramenta_concluir_tarefa
Use quando o usuário quiser marcar uma tarefa como concluída.
Parâmetro necessário:
- id_tarefa

4. ferramenta_consultar_agenda_por_periodo
Use quando o usuário perguntar sobre hoje, amanhã ou essa semana.
Parâmetros:
- periodo: pode ser "hoje", "amanha" ou "essa_semana"
- tipo: opcional, pode ser "aula", "prova", "trabalho" ou null

5. ferramenta_consultar_agenda_por_data
Use quando o usuário perguntar sobre uma data específica, como "dia 25", "sábado" ou "próxima quarta".
Parâmetros:
- texto_data
- tipo: opcional, pode ser "aula", "prova", "trabalho" ou null

6. ferramenta_buscar_material_rag
Use quando o usuário quiser perguntar, resumir ou explicar algo com base nos materiais de estudo.
Use para perguntas como:
- "Explique embeddings"
- "Resuma o conteúdo sobre RAG"
- "O que o material fala sobre inteligência artificial?"
- "Quais são os principais pontos do material?"
Parâmetro necessário:
- pergunta: deve ser a pergunta original do usuário

Regras importantes:

- Responda apenas em JSON, sem explicações.
- Não use markdown.
- Não coloque ```json.
- Não invente nomes de ferramentas.
- Se a ferramenta não precisar de parâmetros, use "parametros": {{}}.
- Para perguntas sobre materiais de estudo, use ferramenta_buscar_material_rag.
- Para perguntas sobre tarefas, use uma das ferramentas de tarefas.
- Para perguntas sobre agenda, use uma das ferramentas de agenda.

Exemplo para agenda:
{{
    "ferramenta": "ferramenta_consultar_agenda_por_periodo",
    "parametros": {{
        "periodo": "essa_semana",
        "tipo": "prova"
    }}
}}

Exemplo para listar tarefas:
{{
    "ferramenta": "ferramenta_listar_tarefas",
    "parametros": {{}}
}}

Exemplo para RAG:
{{
    "ferramenta": "ferramenta_buscar_material_rag",
    "parametros": {{
        "pergunta": "Explique embeddings"
    }}
}}

Pergunta do usuário:
{pergunta_usuario}
"""

    resposta = client.chat.completions.create(
        model="google/gemma-3-12b-it",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return resposta.choices[0].message.content

# Função responsável por gerar uma resposta final amigável para o usuário
def gerar_resposta_final(pergunta_usuario, resultado_ferramenta):
    prompt = f"""
Você é o JARVIS Acadêmico, um assistente inteligente para estudantes.

O usuário fez a seguinte pergunta:

{pergunta_usuario}

O sistema executou uma ferramenta interna e retornou este resultado:

{resultado_ferramenta}

Sua tarefa é responder ao usuário de forma natural, clara e amigável.

Regras:
- Não mencione JSON.
- Não mencione ferramenta.
- Não diga que recebeu dados internos.
- Se o resultado estiver vazio, explique de forma natural que não encontrou nada relacionado à pergunta.
- Se a pergunta for sobre prova e não houver resultado, diga que não encontrou prova cadastrada para aquela data ou período.
- Se a pergunta for sobre aula e não houver resultado, diga que não encontrou aula cadastrada para aquela data ou período.
- Se houver eventos, explique quais são, com data e horário.
- Se houver tarefas, liste as tarefas de forma clara.
- Se uma tarefa foi adicionada, confirme de forma natural.
- Se uma tarefa foi concluída, confirme de forma natural.
- Se for uma resposta de material de estudo, responda com base no conteúdo retornado.
- Responda em português do Brasil.

Resposta final:
"""

    resposta = client.chat.completions.create(
        model="google/gemma-3-12b-it",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return resposta.choices[0].message.content