import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from gemma import perguntar_llm
from pypdf import PdfReader

# Caminho da pasta onde ficam os documentos
CAMINHO_DOCUMENTOS = "data/documentos"

# Esse modelo transforma textos em vetores numéricos para comparação semântica
modelo_embeddings = SentenceTransformer("all-MiniLM-L6-v2")


# Função responsável por extrair texto de arquivos PDF
def extrair_texto_pdf(caminho_arquivo):
    texto_completo = ""

    leitor_pdf = PdfReader(caminho_arquivo)

    for pagina in leitor_pdf.pages:
        texto_pagina = pagina.extract_text()

        if texto_pagina is not None:
            texto_completo = texto_completo + texto_pagina + "\n\n"

    return texto_completo

# Função responsável por carregar arquivos da pasta de documentos
def carregar_documentos():
    documentos = []

    for nome_arquivo in os.listdir(CAMINHO_DOCUMENTOS):
        caminho_arquivo = os.path.join(CAMINHO_DOCUMENTOS, nome_arquivo)

        if nome_arquivo.endswith(".txt"):
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                conteudo = arquivo.read()

            documento = {
                "nome": nome_arquivo,
                "tipo": "txt",
                "conteudo": conteudo
            }

            documentos.append(documento)

        elif nome_arquivo.endswith(".pdf"):
            conteudo = extrair_texto_pdf(caminho_arquivo)

            documento = {
                "nome": nome_arquivo,
                "tipo": "pdf",
                "conteudo": conteudo
            }

            documentos.append(documento)

    return documentos


# Função responsável por dividir o conteúdo em chunks
def dividir_em_chunks(documentos, tamanho_chunk=500):
    chunks = []

    for documento in documentos:
        texto = documento["conteudo"]

        # Divide o texto em parágrafos
        paragrafos = texto.split("\n\n")

        chunk_atual = ""

        for paragrafo in paragrafos:
            # Se o parágrafo ainda cabe no chunk atual
            if len(chunk_atual) + len(paragrafo) <= tamanho_chunk:
                chunk_atual = chunk_atual + "\n\n" + paragrafo
            else:
                # Salva o chunk atual antes de começar outro
                if chunk_atual.strip() != "":
                    chunk = {
                        "documento": documento["nome"],
                        "conteudo": chunk_atual.strip()
                    }

                    chunks.append(chunk)

                # Começa um novo chunk com o parágrafo atual
                chunk_atual = paragrafo

        # Salva o último chunk se tiver conteúdo nele
        if chunk_atual.strip() != "":
            chunk = {
                "documento": documento["nome"],
                "conteudo": chunk_atual.strip()
            }

            chunks.append(chunk)

    return chunks


# Função responsável por gerar embeddings para cada chunk
def gerar_embeddings_chunks(chunks):
    for chunk in chunks:
        texto = chunk["conteudo"]

        # Gera o vetor numérico do texto
        embedding = modelo_embeddings.encode(texto)

        # Salva o embedding dentro do próprio chunk
        chunk["embedding"] = embedding

    return chunks

# Função responsável por normalizar abreviações comuns
def normalizar_pergunta(pergunta):
    pergunta_normalizada = pergunta.lower().strip()

    # Remove sinais 
    pergunta_normalizada = pergunta_normalizada.replace("?", "")
    pergunta_normalizada = pergunta_normalizada.replace("!", "")
    pergunta_normalizada = pergunta_normalizada.replace(".", "")
    pergunta_normalizada = pergunta_normalizada.replace(",", "")

    # abreviações comuns
    abreviacoes = {
        "oq": "o que",
        "q": "que",
        "vc": "você",
        "vcs": "vocês",
        "pq": "por que",
        "tb": "também",
        "tbm": "também",
        "td": "tudo",
        "tds": "todos",
        "blz": "beleza",
        "pfv": "por favor",
        "pff": "por favor",
        "msg": "mensagem",
        "hj": "hoje",
        "amanha": "amanhã",
        "prox": "próximo",
        "proxima": "próxima",
        "info": "informação",
        "infos": "informações",
        "disc": "disciplina",
        "trab": "trabalho",
        "ativ": "atividade",
        "ex": "exemplo",
        "ia": "inteligência artificial",
        "bd": "banco de dados"
    }

    palavras = pergunta_normalizada.split()
    palavras_corrigidas = []

    for palavra in palavras:
        if palavra in abreviacoes:
            palavras_corrigidas.append(abreviacoes[palavra])
        else:
            palavras_corrigidas.append(palavra)

    pergunta_normalizada = " ".join(palavras_corrigidas)

    return pergunta_normalizada

# Função responsável por buscar os chunks mais parecidos com a pergunta
def buscar_chunks_por_embedding(pergunta, chunks, quantidade=3):

    pergunta = normalizar_pergunta(pergunta)

    # Gera o embedding da pergunta
    embedding_pergunta = modelo_embeddings.encode(pergunta)

    resultados = []

    for chunk in chunks:
        embedding_chunk = chunk["embedding"]

        # Calcula a similaridade
        similaridade = cosine_similarity(
            [embedding_pergunta],
            [embedding_chunk]
        )[0][0]

        resultado = {
            "documento": chunk["documento"],
            "conteudo": chunk["conteudo"],
            "similaridade": similaridade
        }

        resultados.append(resultado)

    # Ordena os chunks
    resultados_ordenados = sorted(
        resultados,
        key=lambda item: item["similaridade"],
        reverse=True
    )

    return resultados_ordenados[:quantidade]

# Função responsável por gerar uma resposta usando rag
def gerar_resposta_rag(pergunta, chunks_relevantes):
    contexto = ""

    for indice, chunk in enumerate(chunks_relevantes, start=1):
        contexto = contexto + f"\nTrecho {indice} - Documento: {chunk['documento']}\n"
        contexto = contexto + chunk["conteudo"]
        contexto = contexto + "\n"

    prompt = f"""
    Você é o JARVIS Acadêmico, um assistente de estudos.

    Responda à pergunta do usuário usando apenas os trechos de material fornecidos abaixo.

    Se a resposta não estiver nos trechos, diga que não encontrou informação suficiente nos materiais.

    Trechos recuperados:
    {contexto}

    Pergunta do usuário:
    {pergunta}

    Resposta:
    """

    resposta = perguntar_llm(prompt)

    return resposta