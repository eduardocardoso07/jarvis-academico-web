import os
import sys

import streamlit as st


# Permite importar os arquivos da pasta src
sys.path.append("src")


# Configuração da página
st.set_page_config(
    page_title="JARVIS Acadêmico",
    page_icon="🤖",
    layout="wide"
)


# Quando o app estiver publicado no Streamlit Cloud,
# a chave da Gemma será lida pelos secrets.
if "GEMMA_API_KEY" in st.secrets:
    os.environ["GEMMA_API_KEY"] = st.secrets["GEMMA_API_KEY"]


from gemma import decidir_ferramenta, gerar_resposta_final
from executor import executar_ferramenta


# Estado do histórico do chat
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []


# Função responsável por processar a pergunta do usuário
def processar_pergunta(pergunta):
    historico = ""

    for mensagem in st.session_state.mensagens[-8:]:
        if mensagem["role"] == "user":
            historico = historico + f"Usuário: {mensagem['content']}\n"
        else:
            historico = historico + f"JARVIS: {mensagem['content']}\n"

    pergunta_com_contexto = f"""
Histórico recente da conversa:
{historico}

Mensagem atual do usuário:
{pergunta}
"""

    decisao = decidir_ferramenta(pergunta_com_contexto)
    resultado = executar_ferramenta(decisao)
    resposta_final = gerar_resposta_final(pergunta_com_contexto, resultado)

    return resposta_final


# CSS para melhorar o visual da interface
st.markdown(
    """
    <style>
        .main {
            background-color: #0f172a;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
            max-width: 1100px;
        }

        section[data-testid="stSidebar"] {
            background-color: #020617;
            border-right: 1px solid #1e293b;
        }

        .titulo {
            font-size: 42px;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 0px;
        }

        .subtitulo {
            font-size: 18px;
            color: #cbd5e1;
            margin-bottom: 24px;
        }

        .card {
            background-color: #1e293b;
            padding: 18px;
            border-radius: 16px;
            border: 1px solid #334155;
            color: #e5e7eb;
            margin-bottom: 15px;
        }

        .card h4 {
            margin-bottom: 8px;
            color: #f8fafc;
        }

        .card p {
            color: #cbd5e1;
            font-size: 14px;
        }

        div[data-testid="stChatMessage"] {
            border-radius: 16px;
            padding: 8px;
            margin-bottom: 10px;
        }

        div[data-testid="stChatInput"] {
            background-color: #0f172a;
        }

        .stButton > button {
            border-radius: 12px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Barra lateral fixa com recursos do sistema
with st.sidebar:
    st.markdown("## ⚙️ Recursos")

    st.markdown(
        """
        <div class="card">
            <h4>📚 Materiais de estudo</h4>
            <p>Faça perguntas sobre PDFs e textos adicionados ao projeto.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">
            <h4>🗓️ Agenda acadêmica</h4>
            <p>Consulte aulas, provas e compromissos cadastrados.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="card">
            <h4>✅ Tarefas</h4>
            <p>Adicione, liste e conclua tarefas acadêmicas.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    if st.button("🧹 Limpar conversa", use_container_width=True):
        st.session_state.mensagens = []
        st.rerun()

    st.markdown("---")
    st.markdown("## 📤 Enviar material")

    arquivo_enviado = st.file_uploader(
        "Envie um PDF ou TXT para o JARVIS usar nos estudos",
        type=["pdf", "txt"]
    )

    if arquivo_enviado is not None:
        pasta_documentos = "data/documentos"
        os.makedirs(pasta_documentos, exist_ok=True)

        caminho_arquivo = os.path.join(pasta_documentos, arquivo_enviado.name)

        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(arquivo_enviado.getbuffer())

        st.success(f"Material '{arquivo_enviado.name}' enviado com sucesso!")
        st.info("Agora você já pode fazer perguntas sobre esse material no chat.")

    st.markdown("---")
    st.markdown("## 🧪 Exemplos")

    st.code("Quais são minhas tarefas?")
    st.code("Tenho prova essa semana?")
    st.code("Explique embeddings")
    st.code("Adicione a tarefa revisar RAG")


# Área principal do chat
st.markdown('<h1 class="titulo">🤖 JARVIS Acadêmico</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitulo">Assistente inteligente para tarefas, agenda acadêmica e materiais de estudo.</p>',
    unsafe_allow_html=True
)

st.markdown("### 💬 Converse com o JARVIS")


# Container com rolagem própria para o histórico da conversa
chat_container = st.container(height=620)

with chat_container:
    for mensagem in st.session_state.mensagens:
        with st.chat_message(mensagem["role"]):
            st.markdown(mensagem["content"])


# Campo de digitação do chat
pergunta = st.chat_input("Digite sua pergunta aqui...")

if pergunta:
    st.session_state.mensagens.append(
        {
            "role": "user",
            "content": pergunta
        }
    )

    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        with st.spinner("JARVIS está pensando..."):
            try:
                resposta = processar_pergunta(pergunta)
                st.markdown(resposta)

                st.session_state.mensagens.append(
                    {
                        "role": "assistant",
                        "content": resposta
                    }
                )

            except Exception:
                mensagem_erro = (
                    "Não consegui processar essa solicitação com segurança. "
                    "Pode tentar reformular a pergunta?"
                )

                st.warning(mensagem_erro)

                st.session_state.mensagens.append(
                    {
                        "role": "assistant",
                        "content": mensagem_erro
                    }
                )

    st.rerun()