# Agentic RAG — Multi-Agent Document Intelligence System

A Corrective RAG pipeline built with CrewAI, Groq, Tavily, and HuggingFace embeddings.

## Features
- Upload any PDF and ask questions using a 5-agent pipeline
- Corrective RAG with relevance grading and hallucination checking
- Real-time web search fallback via Tavily
- Trend Analyst agent for current developments
- Report Generator agent for structured document summaries
- Streamlit frontend

## Setup

### Requirements
- Python 3.11
- Groq API key (free at console.groq.com)
- Tavily API key (free at app.tavily.com)

### Installation
```bash
pip install -r requirements.txt
```

### Run the notebook
Open `analysis.ipynb` in Jupyter and add your API keys in Cell 2.

### Run the Streamlit app
```bash
streamlit run app.py
```

### Run with Docker
```bash
docker build -t rag-agent-app .
docker run -p 8501:8501 rag-agent-app
```

## Architecture
5-agent Corrective RAG pipeline:
1. **Router** — decides PDF or web search
2. **Retriever** — fetches relevant information
3. **Grader** — checks relevance
4. **Hallucination Grader** — verifies factual grounding
5. **Answer Synthesiser** — produces final answer