import os
from openai import OpenAI
from dotenv import load_dotenv


# Carrega as variáveis salvas no arquivo .env
load_dotenv()


# Cliente responsável por se conectar com a LLM
client = OpenAI(
    base_url="https://llm.liaufms.org/v1/qwen2-5-14b-instruct-awq",
    api_key=os.getenv("GEMMA_API_KEY")
)


# Nome do modelo usado no endpoint novo
MODELO_LLM = "Qwen/Qwen2.5-14B-Instruct-AWQ"


# Função responsável por enviar uma pergunta simples para a LLM
def perguntar_llm(pergunta):
    resposta = client.chat.completions.create(
        model=MODELO_LLM,
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

7. ferramenta_planejar_estudos
Use quando o usuário pedir um plano de estudos, quiser saber o que priorizar, como organizar os estudos ou como se preparar para uma prova/trabalho.
Use para perguntas como:
- "Monte um plano de estudos para a prova"
- "O que devo priorizar hoje?"
- "Como posso organizar meus estudos esta semana?"
- "Me ajude a estudar para a prova de IA"
Parâmetro necessário:
- objetivo: deve ser a pergunta original do usuário

8. ferramenta_gerar_exercicios

Use quando o usuário quiser exercícios, questões, perguntas para praticar ou testar conhecimento.

Use para perguntas como:
- "Crie exercícios sobre embeddings"
- "Gere 5 questões sobre RAG"
- "Faça perguntas sobre KNN"
- "Monte um simulado de IA"

Parâmetros:
- tema
- quantidade (opcional)

9. ferramenta_avaliar_resposta

Use quando o usuário quiser que o sistema avalie, corrija ou dê feedback sobre uma resposta dele.

Use para perguntas como:
- "Avalie minha resposta sobre embeddings: ..."
- "Corrija minha resposta sobre RAG: ..."
- "Minha resposta está certa? ..."
- "Dê uma nota para minha explicação sobre KNN: ..."

Parâmetros:
- tema
- resposta_usuario

10. resposta_geral
Use quando o usuário fizer uma saudação, agradecimento, pergunta geral ou uma continuação da conversa que não exija necessariamente agenda, tarefas ou materiais.
Use para mensagens como:
- "olá"
- "tudo bem?"
- "obrigado"
- "muito obrigado"
- "somente isso?"
- "o que você faz?"
- "me ajude"

Não use resposta_geral para responder perguntas de conhecimento geral.
Se o usuário perguntar sobre qualquer conteúdo, conceito, pessoa, filme, tecnologia, história, ciência ou assunto externo, use ferramenta_buscar_material_rag.

Parâmetro necessário:
- pergunta: mensagem original do usuário

Regras importantes:

- Responda apenas em JSON, sem explicações.
- Não use markdown.
- Não coloque ```json.
- Não invente nomes de ferramentas.
- Se a ferramenta não precisar de parâmetros, use "parametros": {{}}.
- Para perguntas sobre materiais de estudo, use ferramenta_buscar_material_rag.
- Para perguntas sobre tarefas, use uma das ferramentas de tarefas.
- Para perguntas sobre agenda, use uma das ferramentas de agenda.
- Para pedidos de exercícios, simulados, questões ou perguntas de revisão, use ferramenta_gerar_exercicios, e não escreva "segundo o texto forneciddo..." ou algo semelhante, apenas produza as perguntas.
- Para pedidos de avaliação, correção, nota ou feedback sobre uma resposta do estudante, use ferramenta_avaliar_resposta.
- Para pedidos de plano de estudos, organização de estudos, preparação para prova ou prioridade do dia, use ferramenta_planejar_estudos.
- Se a pergunta for apenas saudação, agradecimento ou conversa geral, use resposta_geral.
- Se o usuário disser "essa", "ela", "essa tarefa" ou "essa também", use o histórico da conversa para tentar entender a referência.
- Se não conseguir identificar uma tarefa específica, use resposta_geral em vez de inventar um ID.

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

Exemplo para planejamento de estudos:
{{
    "ferramenta": "ferramenta_planejar_estudos",
    "parametros": {{
        "objetivo": "Monte um plano de estudos para a prova de IA"
    }}
}}

Exemplo para geração de exercícios:
{{
    "ferramenta": "ferramenta_gerar_exercicios",
    "parametros": {{
        "tema": "embeddings",
        "quantidade": 5
    }}
}}

Exemplo para avaliação de resposta:
{{
    "ferramenta": "ferramenta_avaliar_resposta",
    "parametros": {{
        "tema": "embeddings",
        "resposta_usuario": "Embeddings são números que representam textos."
    }}
}}

Exemplo para resposta geral:
{{ 
    "ferramenta": "resposta_geral",
    "parametros": {{ 
        "pergunta": "muito obrigado"
    }}
}}

Pergunta do usuário:
{pergunta_usuario}
"""

    resposta = client.chat.completions.create(
        model=MODELO_LLM,
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
- Se o resultado tiver objetivo, tarefas, eventos_semana e materiais_relevantes, isso significa que é um planejamento de estudos. Nesse caso, monte um plano organizado com prioridades, horários sugeridos, tarefas pendentes, eventos da semana e materiais recomendados. Não apenas liste os dados: transforme-os em um plano prático de estudo.
- Para planejamento de estudos, priorize primeiro provas e trabalhos próximos, depois tarefas pendentes (sempre comente sobre a importância do tema da tarefa para o planejamento solicitado) e depois revisão dos materiais mais relevantes.
- Se for uma resposta de material de estudo, responda com base no conteúdo retornado.
- Em planejamentos de estudo, só diga que existe prova, aula ou evento marcado se isso aparecer dentro de eventos_semana. Se a informação aparecer apenas em tarefas, trate como tarefa pendente, não como evento confirmado da agenda.
- Ao montar plano de estudos para um tema específico, destaque primeiro tarefas e materiais diretamente relacionados ao tema. Outras tarefas pendentes podem aparecer apenas como prioridades secundárias.
- Responda em português do Brasil.
- Você NÃO deve responder usando conhecimento geral próprio.
- Você só pode responder com base no resultado da ferramenta executada.
- Se o usuário perguntar sobre algo que não esteja nos materiais de estudo, agenda ou tarefas, diga que não encontrou essa informação nos materiais disponíveis.
- Não diga que foi treinado com livros, sites ou textos externos.
- Não mencione base de treinamento.
- Para perguntas gerais como "olá", "obrigado" ou "o que você pode fazer?", responda normalmente e de forma natural.
- Se o resultado tiver "resposta" e "chunks_usados", preserve integralmente o conteúdo de "resposta". Não resuma, não reescreva e não remova partes como "Resposta esperada", "Nota", "Classificação" ou "Resposta ideal".
- Apresente as respostas de uma forma mais organizada, principalmente se for perguntas para gerar exercicios, planejamento de estudos, resumos, apresente com quebra de texto, visualmente bonito e organizado.
Resposta final:
"""

    resposta = client.chat.completions.create(
        model=MODELO_LLM,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return resposta.choices[0].message.content