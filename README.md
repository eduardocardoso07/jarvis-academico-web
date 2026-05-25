# JARVIS Acadêmico

O **JARVIS Acadêmico** é um assistente inteligente desenvolvido para auxiliar estudantes na organização acadêmica, consulta de materiais de estudo e gerenciamento de tarefas.

O projeto foi desenvolvido para a disciplina de **Inteligência Artificial** e utiliza técnicas de:

- RAG (Retrieval-Augmented Generation);
- Tool Calling;
- LLM Gemma 12B;
- embeddings;
- consulta a documentos;
- agenda acadêmica;
- lista de tarefas;
- logs de execução.

---

## Objetivo do projeto

O objetivo do sistema é permitir que o usuário converse com um assistente acadêmico capaz de:

- consultar materiais de estudo;
- responder perguntas com base em documentos;
- listar tarefas;
- adicionar tarefas;
- concluir tarefas;
- consultar agenda acadêmica;
- verificar aulas, provas e compromissos;
- decidir automaticamente qual ferramenta deve ser usada para responder cada pergunta.

O sistema foi construído de forma modular, para que cada parte do projeto fique separada e mais fácil de entender.

---

## Funcionalidades implementadas

## 1. Consulta a materiais de estudo com RAG

O sistema permite que o usuário faça perguntas sobre materiais armazenados na pasta:

```text
data/documentos
```

Exemplos de perguntas:

```text
Explique embeddings
```

```text
Resuma o conteúdo sobre RAG
```

```text
O que o material fala sobre inteligência artificial?
```

O fluxo do RAG funciona da seguinte forma:

1. O sistema carrega os documentos da pasta `data/documentos`;
2. Os documentos são divididos em chunks;
3. O sistema gera embeddings dos chunks;
4. O sistema gera embedding da pergunta do usuário;
5. A pergunta é comparada com os chunks usando similaridade de cosseno;
6. Os trechos mais relevantes são recuperados;
7. Os trechos recuperados são enviados para a Gemma 12B;
8. A Gemma gera uma resposta baseada nos materiais recuperados.

---

## 2. Agenda acadêmica

A agenda acadêmica é armazenada no arquivo:

```text
data/agenda.json
```

O usuário pode perguntar coisas como:

```text
Tenho prova essa semana?
```

```text
O que tenho na próxima quarta?
```

```text
Tenho aula no dia 25?
```

```text
Tenho algo hoje?
```

O sistema consegue consultar:

- eventos de hoje;
- eventos de amanhã;
- eventos da semana atual;
- eventos por data específica;
- eventos por tipo, como `aula`, `prova` ou `trabalho`.

---

## 3. Lista de tarefas

As tarefas são armazenadas no arquivo:

```text
data/tarefas.json
```

O usuário pode pedir:

```text
Quais são minhas tarefas?
```

```text
Adicione a tarefa estudar RAG
```

```text
Marque a tarefa 4 como concluída
```

O sistema consegue:

- adicionar tarefas;
- listar tarefas;
- marcar tarefas como concluídas;
- salvar as alterações no arquivo JSON.

---

## 4. Tool Calling

O sistema usa a LLM **Gemma 12B** para decidir qual ferramenta deve ser chamada.

A Gemma recebe a pergunta do usuário e retorna uma decisão em formato JSON, indicando a ferramenta e os parâmetros necessários.

Exemplo:

```json
{
    "ferramenta": "ferramenta_consultar_agenda_por_periodo",
    "parametros": {
        "periodo": "essa_semana",
        "tipo": "prova"
    }
}
```

Depois disso, o Python executa a ferramenta correspondente.

Esse fluxo garante que a decisão da chamada da ferramenta seja feita pela LLM, e não apenas por uma lógica fixa no código.

---

## 5. Resposta final com LLM

Depois que a ferramenta é executada, o resultado é enviado novamente para a Gemma 12B.

Assim, a resposta final não é uma mensagem fixa do Python. A própria LLM gera uma resposta natural e amigável para o usuário.

Fluxo completo:

```text
Usuário pergunta
↓
Gemma decide a ferramenta
↓
Python executa a ferramenta
↓
Sistema registra log
↓
Gemma gera a resposta final
↓
Usuário recebe uma resposta natural
```

---

## 6. Logs

O sistema registra logs das ferramentas utilizadas no arquivo:

```text
data/logs.json
```

Cada log contém:

- data e hora;
- ferramenta chamada;
- entrada recebida;
- saída retornada.

Exemplo:

```json
{
    "data_hora": "2026-05-25T10:30:00",
    "ferramenta": "ferramenta_listar_tarefas",
    "entrada": {},
    "saida": [
        {
            "id": 1,
            "descricao": "Estudar RAG",
            "concluida": false
        }
    ]
}
```

---

# Estrutura do projeto

```text
jarvis-academico/
│
├── data/
│   ├── documentos/
│   ├── agenda.json
│   ├── tarefas.json
│   └── logs.json
│
├── src/
│   ├── agenda.py
│   ├── datas.py
│   ├── executor.py
│   ├── gemma.py
│   ├── logger.py
│   ├── main.py
│   ├── rag.py
│   ├── tarefas.py
│   └── tools.py
│
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── ANOTACOES_DO_PROJETO.md
```

---

# Explicação dos arquivos

## `src/main.py`

Arquivo principal do sistema.

É responsável por iniciar o JARVIS Acadêmico, receber perguntas do usuário e controlar o fluxo geral do assistente.

Fluxo principal:

1. recebe a pergunta do usuário;
2. envia a pergunta para a Gemma decidir a ferramenta;
3. executa a ferramenta escolhida;
4. envia o resultado para a Gemma gerar a resposta final;
5. mostra a resposta ao usuário.

---

## `src/gemma.py`

Arquivo responsável pela comunicação com a LLM Gemma 12B.

Funções principais:

- `perguntar_llm(pergunta)`: envia uma pergunta simples para a LLM;
- `decidir_ferramenta(pergunta_usuario)`: pede para a Gemma decidir qual ferramenta usar;
- `gerar_resposta_final(pergunta_usuario, resultado_ferramenta)`: gera uma resposta natural com base no resultado da ferramenta.

---

## `src/executor.py`

Arquivo responsável por executar a ferramenta escolhida pela Gemma.

Ele recebe a decisão em JSON, identifica o nome da ferramenta e chama a função correspondente.

Também trata casos em que:

- a Gemma retorna JSON com texto adicional;
- a ferramenta não possui parâmetros;
- o ID da tarefa vem como texto e precisa ser convertido para número.

---

## `src/tools.py`

Arquivo que concentra as ferramentas disponíveis para a LLM.

Ferramentas implementadas:

- `ferramenta_listar_tarefas()`;
- `ferramenta_adicionar_tarefa(descricao)`;
- `ferramenta_concluir_tarefa(id_tarefa)`;
- `ferramenta_consultar_agenda_por_periodo(periodo, tipo=None)`;
- `ferramenta_consultar_agenda_por_data(texto_data, tipo=None)`;
- `ferramenta_buscar_material_rag(pergunta)`.

---

## `src/tarefas.py`

Arquivo responsável pela lista de tarefas.

Funções principais:

- `carregar_tarefas()`;
- `salvar_tarefas(tarefas)`;
- `adicionar_tarefa(descricao)`;
- `listar_tarefas()`;
- `concluir_tarefa(id_tarefa)`.

As tarefas são salvas no arquivo:

```text
data/tarefas.json
```

---

## `src/agenda.py`

Arquivo responsável pela agenda acadêmica.

Funções principais:

- `carregar_agenda()`;
- `listar_eventos()`;
- `buscar_eventos_por_data(data_buscada)`;
- `buscar_eventos_por_periodo(inicio, final)`;
- `filtrar_eventos_por_tipo(eventos, tipo)`.

A agenda é salva no arquivo:

```text
data/agenda.json
```

---

## `src/datas.py`

Arquivo responsável por resolver datas e períodos.

Funções principais:

- `resolver_periodo(periodo)`;
- `resolver_data_especifica(texto_data)`.

A função `resolver_periodo()` entende valores como:

- `hoje`;
- `amanha`;
- `essa_semana`.

A função `resolver_data_especifica()` entende entradas como:

- `dia 25`;
- `segunda`;
- `terça`;
- `quarta`;
- `quinta`;
- `sexta`;
- `sábado`;
- `domingo`;
- `próxima quarta`;
- `sábado que vem`.

Quando o usuário informa um dia da semana, o sistema considera a próxima ocorrência daquele dia.

---

## `src/rag.py`

Arquivo responsável pela implementação do RAG.

Funções principais:

- `carregar_documentos()`;
- `extrair_texto_pdf(caminho_arquivo)`;
- `dividir_em_chunks(documentos)`;
- `gerar_embeddings_chunks(chunks)`;
- `normalizar_pergunta(pergunta)`;
- `buscar_chunks_por_embedding(pergunta, chunks)`;
- `gerar_resposta_rag(pergunta, chunks_relevantes)`.

---

## `src/logger.py`

Arquivo responsável por registrar logs das ferramentas.

Função principal:

- `registrar_log(nome_ferramenta, entrada, saida)`.

Os logs são salvos em:

```text
data/logs.json
```

---

# Dataset

O dataset do projeto fica na pasta:

```text
data/documentos
```

Para a entrega final, essa pasta deve conter pelo menos **10 documentos acadêmicos**.

Os documentos podem estar em formato:

- `.txt`;
- `.pdf`.

---

## Origem dos dados

Os documentos utilizados no dataset devem ser materiais acadêmicos relacionados aos conteúdos estudados.

Exemplos de possíveis origens:

- anotações de aula;
- apostilas;
- materiais disponibilizados pelo professor;
- artigos introdutórios;
- textos próprios produzidos pelo grupo;
- documentos educacionais de fontes abertas.

---

## Tipo de conteúdo

O dataset deve conter conteúdos acadêmicos, como:

- Inteligência Artificial;
- Machine Learning;
- RAG;
- embeddings;
- modelos de linguagem;
- programação;
- banco de dados;
- redes neurais;
- algoritmos;
- engenharia de software.

---

## Limitações do dataset

Algumas limitações do dataset:

- a qualidade das respostas depende da qualidade dos documentos;
- documentos muito curtos podem não fornecer contexto suficiente;
- PDFs com imagens ou texto escaneado podem não ser lidos corretamente;
- o sistema depende da extração textual dos arquivos PDF;
- se a resposta não estiver nos documentos, o sistema pode não encontrar informação suficiente.

---

## Estratégia de chunking

A estratégia de chunking usada no projeto divide os documentos em pedaços menores.

O sistema tenta respeitar os parágrafos, evitando cortar palavras no meio.

Cada chunk possui aproximadamente até 500 caracteres, dependendo do tamanho dos parágrafos.

Essa estratégia foi escolhida porque:

- facilita a recuperação de trechos relevantes;
- evita enviar documentos inteiros para a LLM;
- melhora a qualidade do contexto enviado para a Gemma;
- mantém os trechos mais organizados semanticamente.

---

## Impacto do chunking no RAG

O chunking impacta diretamente a qualidade do RAG.

Chunks muito grandes podem trazer informações desnecessárias.

Chunks muito pequenos podem perder contexto.

Por isso, foi usada uma abordagem intermediária, com chunks baseados em parágrafos e tamanho aproximado.

---

# Como executar o projeto

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

Ativar no Windows:

```bash
.venv\Scripts\activate
```

Ativar no Linux/Mac:

```bash
source .venv/bin/activate
```

---

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

Caso o arquivo `requirements.txt` ainda não exista, instale manualmente:

```bash
pip install openai python-dotenv sentence-transformers scikit-learn pypdf
```

---

## 4. Criar arquivo `.env`

Na raiz do projeto, crie um arquivo chamado:

```text
.env
```

Dentro dele, adicione:

```env
GEMMA_API_KEY=SUA_CHAVE_AQUI
```

A chave real não deve ser enviada para o GitHub.

---

## 5. Executar o sistema

```bash
python src/main.py
```

---

# Exemplos de uso

## Consultar tarefas

```text
Quais são minhas tarefas?
```

---

## Adicionar tarefa

```text
Adicione a tarefa estudar RAG
```

---

## Concluir tarefa

```text
Marque a tarefa 2 como concluída
```

---

## Consultar agenda

```text
Tenho prova essa semana?
```

```text
Tenho aula na próxima quarta?
```

```text
O que tenho hoje?
```

---

## Consultar materiais de estudo

```text
Explique embeddings
```

```text
Resuma o conteúdo sobre RAG
```

```text
O que o material fala sobre inteligência artificial?
```

---

# IAs utilizadas no desenvolvimento

Durante o desenvolvimento do projeto, foram utilizadas ferramentas de IA como apoio.

## ChatGPT

Utilizado para:

- planejamento da arquitetura;
- organização das etapas;
- explicação dos conceitos;
- revisão do código;
- auxílio na documentação;
- sugestões de melhorias;
- apoio na escrita do README.

## Claude / Cursor

Utilizado ou recomendado como apoio para:

- edição de código;
- refatoração;
- revisão de arquivos;
- identificação de bugs;
- organização do projeto.

## Gemma 12B

Utilizada dentro do sistema final como LLM obrigatória do projeto.

A Gemma 12B é responsável por:

- interpretar a pergunta do usuário;
- decidir qual ferramenta chamar;
- gerar respostas finais naturais;
- responder perguntas com base nos trechos recuperados pelo RAG.

---

# Observações de segurança

O arquivo `.env` não deve ser enviado ao GitHub.

Por isso, recomenda-se criar um `.gitignore` com:

```text
.env
.venv/
__pycache__/
*.pyc
data/logs.json
```

---

# Status atual do projeto

Funcionalidades já implementadas:

- lista de tarefas;
- agenda acadêmica;
- tratamento de datas;
- tool calling;
- logs;
- integração com Gemma 12B;
- RAG com documentos `.txt`;
- RAG com suporte a documentos `.pdf`;
- embeddings com `sentence-transformers`;
- busca por similaridade de cosseno;
- resposta final natural gerada pela LLM.

---

# Próximos passos

Possíveis melhorias futuras:

- adicionar mais documentos ao dataset;
- melhorar a interface do usuário;
- criar testes automatizados;
- melhorar tratamento de erros;
- criar avaliação com perguntas de teste;
- analisar falhas do sistema;
- implementar planejamento de estudos;
- adicionar funcionalidades de aprendizado, como exercícios e active recall.

---

# Autoria

Projeto desenvolvido para a disciplina de Inteligência Artificial.

Aluno: Eduardo Teixeira Ribeiro Cardoso
Aluno: Weverton Valério da Silva