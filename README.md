# Telecom Customer Care Chatbot — RAG

A Retrieval-Augmented Generation (RAG) chatbot for telecom customer support.

The chatbot answers customer questions using three knowledge sources:

1. **FAQ data** — general telecom policies and how-to information.
2. **Resolved support tickets** — real customer issues and their resolutions.
3. **Telecom guide PDF** — a longer reference document that is split into searchable chunks.

These sources are embedded with `sentence-transformers/all-MiniLM-L6-v2` and stored in separate Chroma collections. At query time, the application retrieves relevant information from all three collections and sends the combined context to a Groq-hosted language model. The prompt instructs the model to answer only from the retrieved context. fileciteturn1file5L2-L5 fileciteturn1file4L13-L24

---

## Features

- Retrieval-Augmented Generation (RAG)
- Three-source knowledge retrieval
- FAQ semantic search
- Resolved-ticket semantic search
- Telecom PDF semantic search
- Chroma vector database
- Hugging Face sentence-transformer embeddings
- Groq LLM integration
- Streaming responses in the terminal
- Context-restricted answers
- Fallback guidance when retrieved context is insufficient

---

## How the Project Works

The complete flow is:

```text
                         User Question
                              │
                              ▼
                       main.py / CLI
                              │
                              ▼
                        rag_chain.py
                              │
                              ▼
                       retriver.py
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
        FAQ Collection   Tickets Collection  Guides Collection
             │                │                │
             └────────────────┼────────────────┘
                              │
                              ▼
                    Retrieved Documents
                              │
                              ▼
                         RAG Prompt
                              │
                              ▼
                    Groq Language Model
                              │
                              ▼
                     Generated Answer
                              │
                              ▼
                           User
```

The retriever searches the `faq`, `tickets`, and `guides` Chroma collections and combines their results before passing them to the RAG chain. fileciteturn1file5L15-L18 fileciteturn1file5L36-L46

---

# Project Structure

```text
.
├── main.py                 # CLI entry point for the chatbot
├── rag_chain.py            # RAG prompt, retriever, and Groq LLM chain
├── retriver.py             # Merged retriever for all Chroma collections
├── faq_store.py            # FAQ ingestion
├── tickets_store.py        # Resolved-ticket ingestion
├── pdf_store.py            # Telecom PDF ingestion
├── data/
│   ├── faq.csv             # FAQ source data
│   ├── tickets.db          # Resolved support-ticket database
│   └── telecom_guide.pdf   # Telecom reference guide
├── chroma_store/           # Generated Chroma vector-store data
└── .env                    # Groq API key
```

> The exact contents of the `data/` directory must be present for the ingestion scripts to work. The uploaded source files reference `data/faq.csv`, `data/tickets.db`, and `data/telecom_guide.pdf`.

---

# Requirements

You need:

- Python 3.10+ recommended
- A Groq API key
- Internet access for the Groq model and initial Hugging Face embedding-model download
- The required Python packages
- The project's `data/` files

The source code uses:

- LangChain
- LangChain Chroma
- LangChain Hugging Face
- LangChain Groq
- ChromaDB
- Hugging Face sentence-transformer embeddings
- Pandas
- SQLite
- Python dotenv

---

# Complete Setup and Run Process

Follow these steps in order.

## Step 1 — Open the Project

Open a terminal in the project root:

```bash
cd path/to/your/project
```

The directory should contain files such as:

```text
main.py
rag_chain.py
retriver.py
faq_store.py
tickets_store.py
pdf_store.py
```

and the required `data/` directory.

---

## Step 2 — Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, your terminal should show the virtual environment name, for example:

```text
(.venv)
```

---

## Step 3 — Install the Required Packages

Install the project's dependencies:

```bash
pip install -r requirements.txt
```

If your project uses a differently named dependency file, use that file instead.

The source code specifically requires LangChain components, Chroma, Hugging Face embeddings, Groq integration, and related packages.

---

## Step 4 — Configure the Groq API Key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

The application loads environment variables with `python-dotenv`. `main.py` calls `load_dotenv()` before building the chatbot. fileciteturn1file2L5-L11

**Important:** never commit your real API key to GitHub or another public repository.

---

# Step 5 — Check the Data Files

Before running ingestion, make sure these files exist:

```text
data/
├── faq.csv
├── tickets.db
└── telecom_guide.pdf
```

The ingestion scripts directly reference these paths. The FAQ ingestion reads `data/faq.csv`, the ticket ingestion reads `data/tickets.db`, and the PDF ingestion reads `data/telecom_guide.pdf`. fileciteturn1file1L14-L17 fileciteturn1file6L15-L18 fileciteturn1file3L14-L17

---

# Step 6 — Create the FAQ Vector Store

Run the FAQ ingestion script:

```bash
python faq_store.py
```

The script:

1. Reads `data/faq.csv`.
2. Converts each FAQ row into a LangChain `Document`.
3. Stores question and answer text together.
4. Adds metadata such as category and FAQ ID.
5. Generates embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
6. Stores the vectors in the Chroma collection named `faq`.
7. Persists the collection under `chroma_store/`. fileciteturn1file1L19-L27 fileciteturn1file1L30-L43

You should see messages indicating that FAQ documents were loaded and stored.

---

# Step 7 — Create the Resolved Tickets Vector Store

Run:

```bash
python tickets_store.py
```

The ticket ingestion process:

1. Opens `data/tickets.db`.
2. Selects only tickets whose status is `resolved`.
3. Converts each ticket into a document containing the issue type, description, and resolution.
4. Adds ticket metadata.
5. Creates embeddings with `sentence-transformers/all-MiniLM-L6-v2`.
6. Stores the documents in Chroma. fileciteturn1file6L22-L39 fileciteturn1file6L42-L55

Only resolved tickets are used as the support-case knowledge source.

---

# Step 8 — Create the Telecom Guide Vector Store

Run:

```bash
python pdf_store.py
```

The PDF ingestion process:

1. Loads `data/telecom_guide.pdf`.
2. Reads its pages with `PyPDFLoader`.
3. Splits the document using `RecursiveCharacterTextSplitter`.
4. Uses a chunk size of `600`.
5. Uses a chunk overlap of `100`.
6. Adds guide metadata to each chunk.
7. Generates Hugging Face embeddings.
8. Stores the vectors in the Chroma collection `guides`. fileciteturn1file3L9-L20 fileciteturn1file3L23-L54

---

# Step 9 — Verify the Chroma Store

After the three ingestion commands have completed, the project should have a persisted vector store similar to:

```text
chroma_store/
```

with these logical collections:

```text
faq
tickets
guides
```

The retriever opens exactly these three collections. fileciteturn1file5L15-L33

If you change any source data, rerun the corresponding ingestion script so the vector store reflects the updated data.

---

# Step 10 — Start the Chatbot

Run:

```bash
python main.py
```

The CLI starts with:

```text
=== Telecom Customer Care Chatbot (RAG) ===
Type your question and press Enter. Type 'quit' to exit.
```

You can then enter questions interactively. `main.py` builds the RAG chain and streams the generated answer to the terminal. fileciteturn1file2L14-L30

Example:

```text
Customer: How can I troubleshoot my mobile connection?
```

The system retrieves relevant FAQ, ticket, and guide information and uses that context to generate the response.

---

# Step 11 — Exit the Chatbot

To stop the chatbot, type:

```text
quit
```

You can also use:

```text
exit
```

or:

```text
q
```

The CLI handles all three exit commands. fileciteturn1file2L20-L26

---

# RAG Pipeline in Detail

## 1. Data Ingestion

The project has three separate ingestion pipelines.

### FAQ

```text
faq.csv
   │
   ▼
LangChain Documents
   │
   ▼
Hugging Face Embeddings
   │
   ▼
Chroma: faq
```

### Resolved Tickets

```text
tickets.db
   │
   ▼
Resolved tickets only
   │
   ▼
LangChain Documents
   │
   ▼
Hugging Face Embeddings
   │
   ▼
Chroma: tickets
```

### Telecom Guide

```text
telecom_guide.pdf
   │
   ▼
PyPDFLoader
   │
   ▼
RecursiveCharacterTextSplitter
   │
   ▼
Document chunks
   │
   ▼
Hugging Face Embeddings
   │
   ▼
Chroma: guides
```

---

# 2. Retrieval

`retriver.py` creates three Chroma retrievers:

```text
FAQ retriever
Tickets retriever
Guides retriever
```

Each is configured with `k=3` by default, so the merged retriever requests three results from each collection. The results are then concatenated into one list. fileciteturn1file5L18-L23 fileciteturn1file5L36-L46

Conceptually:

```text
User Question
     │
     ├──► FAQ ───────► Top 3
     │
     ├──► Tickets ───► Top 3
     │
     └──► Guides ────► Top 3
                      │
                      ▼
                 Combined Context
```

---

# 3. Prompt Construction

`rag_chain.py` formats the retrieved documents with their source labels.

The prompt distinguishes between:

- `FAQ`
- `TICKETS`
- `GUIDES`

The system prompt tells the model to use **only the retrieved context** when answering. If the context is insufficient, the chatbot is instructed to say so and suggest calling `611` or using the MyTelecom app. fileciteturn1file4L13-L24

---

# 4. LLM Generation

The RAG chain uses a Groq-hosted model configured as:

```text
openai/gpt-oss-120b
```

with:

```text
temperature = 0
max_retries = 2
```

The retrieved context and user question are passed through the prompt and then into the model. fileciteturn1file4L37-L57

---

# Models

## Embedding Model

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This model is used during ingestion and again by the retrievers when searching the Chroma collections. fileciteturn1file1L14-L17 fileciteturn1file5L15-L19

## Generation Model

The RAG response is generated with:

```text
openai/gpt-oss-120b
```

through `ChatGroq`. fileciteturn1file4L44-L50

---

# Example Questions

After starting the chatbot:

```bash
python main.py
```

try questions such as:

```text
How do I troubleshoot my mobile connection?
```

```text
What should I do if I cannot access my mobile service?
```

```text
How can I resolve a billing-related issue?
```

```text
What is the recommended solution for this type of network problem?
```

The actual answer depends on what is present in the indexed FAQ, resolved tickets, and telecom guide.

---

# Updating the Knowledge Base

Whenever the source data changes, rerun the appropriate ingestion script.

## FAQ changed

```bash
python faq_store.py
```

## Tickets database changed

```bash
python tickets_store.py
```

## Telecom PDF changed

```bash
python pdf_store.py
```

Then restart:

```bash
python main.py
```

The ingestion scripts are intended to be run once initially and again whenever their respective source data changes. fileciteturn1file1L1-L3 fileciteturn1file3L2-L5 fileciteturn1file6L1-L3

---

# Troubleshooting

## `GROQ_API_KEY` error

Check that `.env` exists in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Then restart the terminal/application.

---

## `FileNotFoundError` for FAQ data

Check:

```text
data/faq.csv
```

The FAQ ingestion script expects this exact relative path. fileciteturn1file1L14-L17

---

## `FileNotFoundError` for tickets database

Check:

```text
data/tickets.db
```

The ticket ingestion script expects this path. fileciteturn1file6L15-L18

---

## `FileNotFoundError` for the PDF

Check:

```text
data/telecom_guide.pdf
```

The PDF ingestion script expects this path. fileciteturn1file3L14-L17

---

## Chroma collections are missing

Run all three ingestion scripts:

```bash
python faq_store.py
python tickets_store.py
python pdf_store.py
```

Then start the chatbot:

```bash
python main.py
```

---

## The chatbot gives an answer that is not useful

Remember that the system is intentionally context-restricted. The prompt tells the model to answer using only the retrieved FAQ, ticket, and guide context. If the indexed sources do not contain enough information, the model is instructed to say so rather than inventing an answer. fileciteturn1file4L16-L22

Try asking a more specific question related to the telecom knowledge base.

---

# Important Notes

- Run the ingestion scripts **before** running the chatbot for the first time.
- Do not delete `chroma_store/` unless you are prepared to rebuild the vector collections.
- Re-run ingestion after changing the underlying FAQ, ticket, or PDF source.
- Keep the Groq API key private.
- The current chatbot is a terminal/CLI application launched with `python main.py`. fileciteturn1file2L2-L3
- The project uses three independent Chroma collections and merges their retrieved documents at query time. fileciteturn1file5L2-L5

---

# Quick Start

For someone who just wants the shortest working process:

```bash
# 1. Create environment
python -m venv .venv

# 2. Activate environment — Windows
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure .env
# GROQ_API_KEY=your_groq_api_key_here

# 5. Build FAQ vectors
python faq_store.py

# 6. Build ticket vectors
python tickets_store.py

# 7. Build PDF vectors
python pdf_store.py

# 8. Start chatbot
python main.py
```

Then ask your telecom support question.

---

# License

No license information was provided in the supplied project files.
