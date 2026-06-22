# JARVIS Acadêmico

O **JARVIS Acadêmico** é um assistente inteligente desenvolvido para auxiliar estudantes na organização acadêmica, consulta de materiais de estudo e gerenciamento de atividades.

O projeto foi desenvolvido para a disciplina de **Inteligência Artificial** e integra técnicas modernas como:

* Retrieval-Augmented Generation (RAG)
* Tool Calling
* Large Language Models (LLMs)
* Embeddings
* Busca Vetorial
* Planejamento de Estudos
* Active Recall
* Interface Web com Streamlit

---

# Objetivo do Projeto

O objetivo do sistema é fornecer um assistente acadêmico capaz de:

* responder perguntas sobre materiais de estudo;
* consultar documentos PDF e TXT;
* gerenciar tarefas acadêmicas;
* consultar agenda de aulas, provas e trabalhos;
* gerar planos de estudo personalizados;
* criar exercícios automaticamente;
* avaliar respostas dos estudantes;
* auxiliar na preparação para provas e trabalhos.

---

# Funcionalidades Implementadas

## 1. Consulta a Materiais com RAG

O sistema permite que o usuário faça perguntas sobre documentos armazenados na pasta:

```text
data/documentos
```

Exemplos:

```text
O que são embeddings?
```

```text
Explique RAG.
```

```text
Como funciona o algoritmo KNN?
```

Fluxo utilizado:

1. Carregamento dos documentos.
2. Divisão em chunks.
3. Geração de embeddings.
4. Busca vetorial por similaridade.
5. Recuperação dos trechos relevantes.
6. Geração da resposta pela LLM.

---

## 2. Agenda Acadêmica

Os eventos são armazenados em:

```text
data/agenda.json
```

Exemplos:

```text
Tenho prova essa semana?
```

```text
O que tenho hoje?
```

```text
Tenho aula na próxima quarta?
```

O sistema permite:

* consultar eventos por data;
* consultar eventos por período;
* filtrar eventos por tipo;
* visualizar aulas, provas e trabalhos.

---

## 3. Gerenciamento de Tarefas

As tarefas são armazenadas em:

```text
data/tarefas.json
```

Exemplos:

```text
Quais são minhas tarefas?
```

```text
Adicione a tarefa revisar embeddings.
```

```text
Marque a tarefa 2 como concluída.
```

Funcionalidades:

* adicionar tarefas;
* listar tarefas;
* concluir tarefas;
* persistir dados em JSON.

---

## 4. Planejamento de Estudos

O sistema gera planos de estudo utilizando:

* tarefas pendentes;
* agenda acadêmica;
* materiais recuperados pelo RAG.

Exemplos:

```text
O que devo priorizar hoje?
```

```text
Me gere um plano de estudos para a prova de IA.
```

---

## 5. Geração Automática de Exercícios

O sistema pode criar exercícios utilizando os materiais disponíveis.

Exemplos:

```text
Crie 3 exercícios sobre RAG.
```

```text
Gere 5 perguntas sobre embeddings.
```

Cada exercício é acompanhado de uma resposta esperada.

---

## 6. Active Recall

O sistema avalia respostas fornecidas pelo estudante.

Exemplo:

```text
Avalie minha resposta sobre embeddings:
embeddings são representações numéricas de textos
```

A avaliação inclui:

* classificação;
* nota;
* pontos positivos;
* pontos que precisam melhorar;
* resposta ideal.

---

## 7. Tool Calling

A LLM Gemma 12B é responsável por decidir qual ferramenta deve ser utilizada.

Exemplo:

```json
{
    "ferramenta": "ferramenta_listar_tarefas",
    "parametros": {}
}
```

Após a decisão da LLM, o Python executa a ferramenta correspondente e retorna o resultado para geração da resposta final.

---

## 8. Logs

Todas as ferramentas utilizadas são registradas em:

```text
data/logs.json
```

Cada log armazena:

* data e hora;
* ferramenta utilizada;
* entrada recebida;
* saída retornada.

Isso permite rastrear e analisar o comportamento do sistema.

---

# Interface Web

A aplicação utiliza **Streamlit** para fornecer uma interface moderna e responsiva.

Recursos disponíveis:

* chat com o assistente;
* upload de PDFs e TXT;
* histórico da conversa;
* limpeza da conversa;
* exibição dos recursos do sistema;
* interação por linguagem natural.

---

# Estrutura do Projeto

```text
jarvis-academico/
│
├── data/
│   ├── agenda.json
│   ├── tarefas.json
│   ├── logs.json
│   └── documentos/
│
├── src/
│   ├── agenda.py
│   ├── executor.py
│   ├── gemma.py
│   ├── logger.py
│   ├── rag.py
│   ├── tarefas.py
│   └── tools.py
│
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .env.exemplo
└── .gitignore
```

---

# Dataset

Os documentos utilizados pelo sistema ficam em:

```text
data/documentos
```

O conjunto de documentos inclui conteúdos sobre:

* Inteligência Artificial;
* Machine Learning;
* Processamento de Linguagem Natural;
* Embeddings;
* Busca Semântica;
* RAG;
* Modelos de Linguagem;
* Engenharia de Prompt;
* KNN;
* Agentes Inteligentes;
* Ética em IA.

Os documentos são utilizados como base de conhecimento para o sistema RAG.

---

# Como Executar o Projeto

## 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd jarvis-academico
```

---

## 2. Criar ambiente virtual

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 4. Configurar a API

Crie um arquivo `.env` utilizando como base o arquivo `.env.exemplo`.

Exemplo:

```env
GEMMA_API_KEY=sua_chave_aqui
```

O arquivo `.env` não deve ser enviado para o GitHub.

---

## 5. Executar a aplicação

```bash
streamlit run streamlit_app.py
```

---

# Exemplos de Uso

## Consulta de Conteúdo

```text
O que são embeddings?
```

```text
Explique RAG.
```

---

## Tarefas

```text
Quais são minhas tarefas?
```

```text
Adicione a tarefa estudar KNN.
```

---

## Agenda

```text
Tenho prova essa semana?
```

---

## Planejamento

```text
O que devo priorizar hoje?
```

```text
Me gere um plano de estudos para a prova de IA.
```

---

## Exercícios

```text
Crie 3 exercícios sobre RAG.
```

---

## Active Recall

```text
Avalie minha resposta sobre embeddings:
embeddings são números usados para representar textos
```

---

# Tecnologias Utilizadas

* Python
* Streamlit
* Gemma 12B
* Sentence Transformers
* Scikit-Learn
* PyPDF
* NumPy
* JSON

---

# Status Atual do Projeto

Funcionalidades implementadas:

* Consulta de materiais via RAG;
* Embeddings e busca vetorial;
* Tool Calling com Gemma 12B;
* Agenda acadêmica;
* Gerenciamento de tarefas;
* Planejamento de estudos;
* Geração automática de exercícios;
* Avaliação de respostas (Active Recall);
* Logs de execução;
* Interface Web responsiva com Streamlit;
* Upload de documentos PDF e TXT.

---

# Possíveis Melhorias Futuras

* reranking dos documentos recuperados;
* estatísticas de desempenho do estudante;
* revisão espaçada;
* simulados automáticos;
* integração com calendários externos;
* dashboard acadêmico.

---

# Autoria

Projeto desenvolvido para a disciplina de Inteligência Artificial.

**Eduardo Teixeira Ribeiro Cardoso**

**Weverton Valério da Silva**
