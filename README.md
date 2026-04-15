# ResearchMind

An AI-powered multi-agent system that generates comprehensive Literature Reviews from any research topic — automatically searching, reading, analyzing, and writing academic content.

---

## What it does

You give it a research topic. It gives you a full Literature Review.

Behind the scenes, four specialized AI agents collaborate in a pipeline:

- **Search Agent** — finds recent academic papers using Tavily
- **Reader Agent** — reads and summarizes each paper
- **Analyzer Agent** — compares methodologies, identifies gaps and trends
- **Writer Agent** — produces a structured, academic-style Literature Review

The result is a ready-to-use report with real references, research gaps, current trends, and future directions.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Orchestration | LangGraph (multi-agent) |
| LLM | Groq — Llama 3.3 70B |
| Search | Tavily API |
| Backend | FastAPI |
| Frontend | Streamlit |
| Auth & Database | Supabase |
| Observability | Langfuse |
| Containerization | Docker |

---

## Architecture

```
User Input (topic)
      ↓
Supervisor Agent  ←  decides who works next
      ↓
┌─────────────────────────────────────┐
│  Search → Reader → Analyzer → Writer │
└─────────────────────────────────────┘
      ↓
Literature Review (streamed in real-time)
```

The system uses a **supervisor pattern** — a central agent that routes work to specialized agents based on the current state, with full checkpointing and error handling.

---

## Features

- **Real-time streaming** — watch the report being written token by token
- **Multi-agent pipeline** — each agent has a single, well-defined responsibility
- **Prompt injection protection** — input validation at multiple layers
- **Authentication** — JWT-based auth via Supabase
- **Report history** — every generated report is saved per user
- **Observability** — full tracing of every agent run via Langfuse
- **Rate limiting** — prevents API abuse
- **Async throughout** — built for concurrent users

---

## Project Structure

```
ResearchMind/
├── agents/                 # AI agents + prompts
│   ├── prompts/            # separated prompt templates
│   ├── supervisor.py
│   ├── search_agent.py
│   ├── reader_agent.py
│   ├── analyzer_agent.py
│   ├── writer_agent.py
│   ├── llm.py
│   └── state.py
├── api/                    # FastAPI application
│   ├── routes/             # endpoints
│   ├── services/           # business logic
│   ├── schemas/            # request/response models
│   ├── main.py
│   ├── auth.py
│   ├── limiter.py
│   └── dependencies.py
│   
├── frontend/               # Streamlit UI
│   ├── pages/
│   └── services/
├── repositories/           # database layer
├── tools/           
├── utils/                  # shared utilities
├── graph.py                # LangGraph pipeline
└── Dockerfile
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker (optional)
- API keys: Groq, Tavily, Supabase, Langfuse

### Installation

```bash
git clone https://github.com/MakdadTaleb/ResearchMind.git
cd ResearchMind
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
cp .env.example .env
```

### Run

```bash
# API
uvicorn api.main:api --reload

# Frontend (separate terminal)
streamlit run frontend/app.py
```

### Run with Docker

```bash
docker build -t researchmind .
docker run -p 8000:8000 -p 8501:8501 --env-file .env researchmind
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Login, returns JWT |
| POST | `/research` | Generate Literature Review |
| POST | `/research/stream` | Generate with real-time streaming |
| GET | `/research/reports` | Get user's report history |
| GET | `/research/reports/{id}` | Get specific report |
| GET | `/health` | Check server health |

---

## Design Decisions

**Why LangGraph?** — The research pipeline is inherently stateful and sequential. LangGraph gives full control over agent routing, state management, and checkpointing — things that are painful to implement manually.

**Why a Supervisor pattern?** — Each agent does one thing well. The supervisor decides what happens next based on state, making it easy to add new agents or handle failures without changing existing code.

**Why Groq?** — Speed. Literature review generation involves multiple LLM calls in sequence. Groq's inference speed makes the pipeline feel responsive rather than painful.

**Why separate prompts from agent logic?** — Prompts change often during development. Separating them means you can iterate on prompts without touching the agent's execution logic.

---

## Author

**Makdad Taleb** — AI Engineer  
[LinkedIn](https://linkedin.com/in/makdadtaleb) · [GitHub](https://github.com/MakdadTaleb) · [HuggingFace](https://huggingface.co/makdadTaleb)
