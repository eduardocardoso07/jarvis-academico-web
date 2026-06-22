import os
import sys

import streamlit as st
from dotenv import load_dotenv

load_dotenv()
sys.path.append("src")

st.set_page_config(
    page_title="JARVIS Acadêmico",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "GEMMA_API_KEY" in st.secrets:
    os.environ["GEMMA_API_KEY"] = st.secrets["GEMMA_API_KEY"]

from gemma import decidir_ferramenta, gerar_resposta_final
from executor import executar_ferramenta


if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if "active_recall" not in st.session_state:
    st.session_state.active_recall = {
        "ativo": False,
        "pergunta": "",
        "resposta_esperada": "",
        "tema": ""
    }


def processar_pergunta(pergunta):
    historico = ""

    for mensagem in st.session_state.mensagens[-8:]:
        if mensagem["role"] == "user":
            historico += f"Usuário: {mensagem['content']}\n"
        else:
            historico += f"JARVIS: {mensagem['content']}\n"

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


st.markdown(
    """
    <style>
        :root {
            --bg: #0f172a;
            --panel: #111827;
            --card: #1e293b;
            --card2: #0f172a;
            --border: #334155;
            --text: #f8fafc;
            --muted: #cbd5e1;
            --accent: #38bdf8;
            --green: #22c55e;
            --yellow: #facc15;
            --purple: #a78bfa;
        }

        .stApp {
            background: radial-gradient(circle at top left, #1e293b 0, #0f172a 35%, #020617 100%);
            color: var(--text);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.5rem;
            padding-bottom: 1rem;
        }

        section[data-testid="stSidebar"] {
            background: #020617;
            border-right: 1px solid #1e293b;
        }

        .hero {
            padding: 22px 24px;
            border-radius: 24px;
            border: 1px solid rgba(148, 163, 184, .25);
            background: linear-gradient(135deg, rgba(56,189,248,.14), rgba(167,139,250,.10));
            margin-bottom: 18px;
        }

        .titulo {
            font-size: clamp(30px, 5vw, 48px);
            font-weight: 900;
            color: #f8fafc;
            margin: 0;
            line-height: 1.05;
        }

        .subtitulo {
            font-size: clamp(15px, 2.5vw, 18px);
            color: #cbd5e1;
            margin-top: 10px;
            max-width: 820px;
        }

        .badge {
            display: inline-block;
            padding: 6px 10px;
            margin: 6px 6px 0 0;
            border-radius: 999px;
            background: rgba(56, 189, 248, .12);
            color: #bae6fd;
            border: 1px solid rgba(56, 189, 248, .25);
            font-size: 13px;
            font-weight: 700;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin: 14px 0 22px 0;
        }

        .feature-card {
            background: rgba(30, 41, 59, .84);
            border: 1px solid rgba(148, 163, 184, .22);
            padding: 16px;
            border-radius: 18px;
            min-height: 138px;
        }

        .feature-card h4 {
            color: #f8fafc;
            margin: 0 0 8px 0;
            font-size: 17px;
        }

        .feature-card p {
            color: #cbd5e1;
            font-size: 14px;
            margin: 0;
            line-height: 1.45;
        }

        .sidebar-card {
            background: #111827;
            border: 1px solid #334155;
            padding: 14px;
            border-radius: 16px;
            margin-bottom: 12px;
        }

        .sidebar-card h4 {
            margin: 0 0 6px 0;
            color: #f8fafc;
            font-size: 15px;
        }

        .sidebar-card p {
            margin: 0;
            color: #cbd5e1;
            font-size: 13px;
        }

        div[data-testid="stChatMessage"] {
            border-radius: 18px;
            padding: 8px;
            margin-bottom: 12px;
            border: 1px solid rgba(148, 163, 184, .12);
            background: rgba(15, 23, 42, .45);
        }

        div[data-testid="stChatInput"] {
            background-color: transparent;
        }

        .stButton > button {
            border-radius: 12px;
            font-weight: 700;
            border: 1px solid #334155;
        }

        .small-help {
            color: #94a3b8;
            font-size: 13px;
            margin-top: -6px;
            margin-bottom: 10px;
        }

        @media (max-width: 900px) {
            .grid {
                grid-template-columns: 1fr;
            }

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hero {
                padding: 18px;
            }
        }

        @media (max-width: 600px) {
            .titulo {
                font-size: 32px;
            }

            .subtitulo {
                font-size: 15px;
            }

            .feature-card {
                min-height: auto;
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.markdown("## ⚙️ Painel do JARVIS")

    st.markdown(
        """
        <div class="sidebar-card">
            <h4>📚 RAG</h4>
            <p>Consulta PDFs e textos usando chunks, embeddings e recuperação semântica.</p>
        </div>
        <div class="sidebar-card">
            <h4>🗓️ Agenda</h4>
            <p>Consulta aulas, provas e entregas acadêmicas.</p>
        </div>
        <div class="sidebar-card">
            <h4>✅ Tarefas</h4>
            <p>Adiciona, lista e conclui tarefas do estudante.</p>
        </div>
        <div class="sidebar-card">
            <h4>🧠 Planejamento de Estudos</h4>
            <p>Planejamento de estudos, exercícios e avaliação de respostas.</p>
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
        "Envie um PDF ou TXT",
        type=["pdf", "txt"]
    )

    if arquivo_enviado is not None:
        pasta_documentos = "data/documentos"
        os.makedirs(pasta_documentos, exist_ok=True)

        caminho_arquivo = os.path.join(pasta_documentos, arquivo_enviado.name)

        with open(caminho_arquivo, "wb") as arquivo:
            arquivo.write(arquivo_enviado.getbuffer())

        st.success(f"Material '{arquivo_enviado.name}' enviado.")
        st.info("Agora ele já pode ser usado pelo RAG.")

    st.markdown("---")
    st.markdown("## 🧪 Exemplos rápidos")

    exemplos = [
        "Monte um plano de estudos para a prova de IA",
        "O que devo priorizar hoje?",
        "Crie 5 exercícios sobre embeddings",
        "Avalie minha resposta sobre RAG: RAG combina busca e geração",
        "Explique o que são embeddings",
        "Quais são minhas tarefas?",
        "Tenho prova essa semana?"
    ]

    for exemplo in exemplos:
        st.code(exemplo, language=None)


st.markdown(
    """
    <div class="hero">
        <h1 class="titulo">🤖 JARVIS Acadêmico</h1>
        <p class="subtitulo">
            Assistente inteligente para estudantes com RAG, Tool Calling, agenda,
            tarefas, planejamento de estudos e funcionalidades de aprendizagem.
        </p>
        <span class="badge">RAG</span>
        <span class="badge">Tool Calling</span>
        <span class="badge">Gemma / LLM</span>
        <span class="badge">Planejamento</span>
        <span class="badge">Exercícios</span>
        <span class="badge">Feedback</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="grid">
        <div class="feature-card">
            <h4>📘 Consulta aos materiais</h4>
            <p>Faça perguntas sobre PDFs e textos. O sistema recupera trechos relevantes e responde com base neles.</p>
        </div>
        <div class="feature-card">
            <h4>🧭 Planejamento de estudos</h4>
            <p>Combina agenda, tarefas e materiais para sugerir prioridades e organizar a preparação do estudante.</p>
        </div>
        <div class="feature-card">
            <h4>🧠 Aprendizado ativo</h4>
            <p>Gera exercícios e avalia respostas do aluno com nota, feedback e resposta ideal.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("### 💬 Converse com o JARVIS")
st.markdown(
    '<p class="small-help">Digite perguntas sobre materiais, agenda, tarefas, planejamento, exercícios ou avaliação de respostas.</p>',
    unsafe_allow_html=True
)

chat_container = st.container(height=560)

with chat_container:
    if len(st.session_state.mensagens) == 0:
        st.info("Comece perguntando: “Monte um plano de estudos para a prova de IA” ou “Crie exercícios sobre embeddings”.")
    else:
        for mensagem in st.session_state.mensagens:
            with st.chat_message(mensagem["role"]):
                st.markdown(mensagem["content"])


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

            except Exception as erro:
                mensagem_erro = (
                    "Não consegui processar essa solicitação com segurança. "
                    "Verifique se os arquivos JSON estão válidos e tente novamente."
                )

                st.warning(mensagem_erro)

                st.session_state.mensagens.append(
                    {
                        "role": "assistant",
                        "content": mensagem_erro
                    }
                )

    st.rerun()