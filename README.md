# 🧠 Adaptive RAG — LangGraph-Powered Agentic Chatbot

An intelligent Retrieval-Augmented Generation (RAG) system that 
dynamically routes user queries to the most appropriate knowledge 
source using LangGraph-powered agentic workflows.

## 🚀 Live Demo
Upload any PDF → Ask questions → Get intelligent answers

## ⚙️ How It Works

User Query → LangGraph Router
├── 📚 Index Route    → Searches uploaded documents (Qdrant)
├── 🧠 General Route  → Answers using LLM knowledge (Groq)
└── 🌐 Search Route   → Fetches real-time web results (Tavily)

Each route includes:
- Document grading (relevance checking)
- Query rewriting (if no relevant docs found)
- Answer generation (Llama 3.3 70B via Groq)

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Agentic Workflow | LangGraph |
| LLM | Groq (Llama 3.3 70B) |
| Vector Database | Qdrant Cloud |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Web Search | Tavily API |
| Chat Memory | MongoDB Atlas |
| Backend | FastAPI |
| Frontend | Streamlit |

## 📁 Project Structure
AdaptiveRag/
├── src/
│   ├── api/          # FastAPI routes
│   ├── config/       # Settings and prompts
│   ├── core/         # Logger
│   ├── db/           # MongoDB client
│   ├── llms/         # Groq LLM setup
│   ├── memory/       # Chat history
│   ├── models/       # Pydantic schemas
│   └── rag/          # Core RAG pipeline
│       ├── graph_builder.py  # LangGraph workflow
│       ├── nodes.py          # Agent nodes
│       ├── retriever_setup.py
│       └── document_upload.py
└── streamlit_app/    # Frontend UI

## 🔧 Setup & Installation

1. Clone the repo
```bash
git clone https://github.com/varun0852/AdaptiveRag.git
cd AdaptiveRag
```

2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key
QDRANT_URL=your_url
QDRANT_API_KEY=your_key
QDRANT_DOCS_COLLECTION=documents
MONGODB_URL=your_url
MONGODB_DB_NAME=adaptive_rag

5. Run the backend
```bash
uvicorn src.main:app --reload --port 8000
```

6. Run the frontend
```bash
streamlit run streamlit_app/home.py
```

## ✨ Features
- 🔀 Adaptive query routing (3 routes)
- 📄 PDF and TXT document upload & indexing
- ✅ Document relevance grading
- 🔁 Automatic query rewriting
- 💬 Persistent chat history per session
- 🌐 Real-time web search integration

## 👤 Author
Varun Diwakar — AI/ML Engineer
