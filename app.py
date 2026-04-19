import streamlit as st
import os
import tempfile

st.set_page_config(
    page_title="RAG Agent System",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a26;
    --border: #2a2a3e;
    --border2: #3a3a55;
    --accent: #7c6af7;
    --accent2: #a594ff;
    --accent3: #4de8c2;
    --text: #e8e6f0;
    --text2: #9896b0;
    --text3: #5a5870;
    --success: #4de8c2;
    --warning: #f7c26a;
    --danger: #f76a8a;
}

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: var(--bg);
    color: var(--text);
}

.stApp {
    background: var(--bg);
}

/* Hide streamlit defaults */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Custom header */
.app-header {
    padding: 2.5rem 0 1.5rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.app-header h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    letter-spacing: -0.03em;
    color: var(--text);
    margin: 0;
    line-height: 1.1;
}
.app-header h1 span {
    color: var(--accent2);
}
.app-header p {
    color: var(--text2);
    font-size: 0.85rem;
    margin: 0.5rem 0 0 0;
    letter-spacing: 0.05em;
}

/* Section labels */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Agent mode cards */
.mode-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.mode-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem 1.1rem;
    cursor: pointer;
    transition: all 0.15s ease;
    position: relative;
    overflow: hidden;
}
.mode-card:hover {
    border-color: var(--border2);
    background: var(--surface2);
}
.mode-card.selected {
    border-color: var(--accent);
    background: rgba(124, 106, 247, 0.08);
}
.mode-card.selected::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
}
.mode-icon {
    font-size: 1.3rem;
    margin-bottom: 0.4rem;
}
.mode-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.85rem;
    color: var(--text);
    margin-bottom: 0.2rem;
}
.mode-desc {
    font-size: 0.72rem;
    color: var(--text3);
    line-height: 1.4;
}

/* Upload zone */
.upload-zone {
    border: 1px dashed var(--border2);
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    background: var(--surface);
    margin-bottom: 1rem;
    transition: border-color 0.15s;
}
.upload-zone:hover {
    border-color: var(--accent);
}

/* Streamlit widget overrides */
.stFileUploader > div {
    background: var(--surface) !important;
    border: 1px dashed var(--border2) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}
.stFileUploader label {
    color: var(--text2) !important;
    font-size: 0.8rem !important;
}
.stTextInput > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
.stTextInput > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.15) !important;
}
.stTextInput input {
    color: var(--text) !important;
    background: transparent !important;
}
.stTextInput label {
    color: var(--text2) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* Button */
.stButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.6rem 1.8rem !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--accent2) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(124,106,247,0.3) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Radio buttons */
.stRadio > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 0.75rem !important;
}
.stRadio label {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 0.4rem 0.8rem !important;
    cursor: pointer !important;
    font-size: 0.78rem !important;
    color: var(--text2) !important;
    transition: all 0.15s !important;
}
.stRadio label:hover {
    border-color: var(--accent) !important;
    color: var(--text) !important;
}

/* Answer output */
.answer-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent3);
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 1.5rem;
    font-size: 0.88rem;
    line-height: 1.7;
    color: var(--text);
}
.answer-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid var(--border);
}
.answer-header-label {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.8rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--accent3);
}
.answer-badge {
    margin-left: auto;
    font-size: 0.65rem;
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    background: rgba(77, 232, 194, 0.1);
    color: var(--accent3);
    border: 1px solid rgba(77, 232, 194, 0.2);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Agent pipeline viz */
.pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 1rem 0;
    overflow-x: auto;
    padding-bottom: 0.5rem;
}
.pipeline-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
    min-width: 80px;
}
.pipeline-node {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    border: 1px solid var(--border);
    background: var(--surface);
}
.pipeline-node.active {
    border-color: var(--accent);
    background: rgba(124,106,247,0.1);
    box-shadow: 0 0 12px rgba(124,106,247,0.2);
}
.pipeline-label {
    font-size: 0.58rem;
    color: var(--text3);
    text-align: center;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    white-space: nowrap;
}
.pipeline-arrow {
    font-size: 0.7rem;
    color: var(--border2);
    padding: 0 0.2rem;
    margin-bottom: 1rem;
}

/* Sidebar */
.css-1d391kg, [data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] .stTextInput > div > div {
    background: var(--bg) !important;
}

/* PDF info card */
.pdf-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
}
.pdf-icon {
    width: 32px;
    height: 32px;
    background: rgba(124,106,247,0.1);
    border: 1px solid rgba(124,106,247,0.2);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}
.pdf-name {
    font-size: 0.82rem;
    color: var(--text);
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.pdf-size {
    font-size: 0.7rem;
    color: var(--text3);
}

/* Status indicators */
.status-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}
.status-pill {
    font-size: 0.7rem;
    padding: 0.25rem 0.6rem;
    border-radius: 20px;
    display: flex;
    align-items: center;
    gap: 0.3rem;
}
.status-pill.ok {
    background: rgba(77,232,194,0.08);
    color: var(--accent3);
    border: 1px solid rgba(77,232,194,0.2);
}
.status-pill.warn {
    background: rgba(247,194,106,0.08);
    color: var(--warning);
    border: 1px solid rgba(247,194,106,0.2);
}
.dot { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }

/* Spinner override */
.stSpinner > div {
    border-top-color: var(--accent) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}

/* Divider */
hr {
    border-color: var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* Alerts */
.stSuccess > div {
    background: rgba(77,232,194,0.08) !important;
    border: 1px solid rgba(77,232,194,0.2) !important;
    color: var(--accent3) !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
}
.stError > div {
    background: rgba(247,106,138,0.08) !important;
    border: 1px solid rgba(247,106,138,0.2) !important;
    color: var(--danger) !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
}
.stWarning > div {
    background: rgba(247,194,106,0.08) !important;
    border: 1px solid rgba(247,194,106,0.2) !important;
    color: var(--warning) !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-header">
    <h1>⬡ Agentic <span>RAG</span></h1>
    <p>MULTI-AGENT DOCUMENT INTELLIGENCE SYSTEM</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="section-label">API Configuration</div>', unsafe_allow_html=True)
    groq_key = st.text_input("GROQ API KEY", type="password", placeholder="gsk_...")
    tavily_key = st.text_input("TAVILY API KEY", type="password", placeholder="tvly-...")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Agent Pipeline</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pipeline">
        <div class="pipeline-step">
            <div class="pipeline-node active">🔀</div>
            <div class="pipeline-label">Router</div>
        </div>
        <div class="pipeline-arrow">›</div>
        <div class="pipeline-step">
            <div class="pipeline-node active">🔍</div>
            <div class="pipeline-label">Retriever</div>
        </div>
        <div class="pipeline-arrow">›</div>
        <div class="pipeline-step">
            <div class="pipeline-node active">✓</div>
            <div class="pipeline-label">Grader</div>
        </div>
        <div class="pipeline-arrow">›</div>
        <div class="pipeline-step">
            <div class="pipeline-node active">🧠</div>
            <div class="pipeline-label">Halluc.</div>
        </div>
        <div class="pipeline-arrow">›</div>
        <div class="pipeline-step">
            <div class="pipeline-node active">💬</div>
            <div class="pipeline-label">Answer</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Status</div>', unsafe_allow_html=True)

    groq_ok = bool(groq_key and groq_key.startswith("gsk_"))
    tavily_ok = bool(tavily_key and tavily_key.startswith("tvly-"))

    st.markdown(f"""
    <div class="status-row">
        <div class="status-pill {'ok' if groq_ok else 'warn'}">
            <div class="dot"></div>
            Groq {'ready' if groq_ok else 'missing'}
        </div>
        <div class="status-pill {'ok' if tavily_ok else 'warn'}">
            <div class="dot"></div>
            Tavily {'ready' if tavily_ok else 'missing'}
        </div>
    </div>
    """, unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="section-label">Document</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload PDF",
        type="pdf",
        label_visibility="collapsed"
    )

    if uploaded_file:
        size_kb = len(uploaded_file.getvalue()) / 1024
        st.markdown(f"""
        <div class="pdf-card">
            <div class="pdf-icon">📄</div>
            <div>
                <div class="pdf-name">{uploaded_file.name}</div>
                <div class="pdf-size">{size_kb:.1f} KB · PDF</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Agent Mode</div>', unsafe_allow_html=True)

    mode = st.radio(
        "Select mode",
        options=["5-Agent RAG Pipeline", "Trend Analyst", "Report Generator"],
        label_visibility="collapsed",
        horizontal=False
    )

    mode_info = {
        "5-Agent RAG Pipeline": "Routes your question to the PDF or web, retrieves relevant information, grades it for relevance and hallucinations, then returns a verified answer.",
        "Trend Analyst": "Searches the web for the latest trends and developments related to the topic of your uploaded document.",
        "Report Generator": "Reads your document and automatically generates a structured markdown report covering key findings, insights, and challenges."
    }

    st.markdown(f"""
    <div style="background: var(--surface); border: 1px solid var(--border);
                border-radius: 6px; padding: 0.75rem 1rem; margin-top: 0.5rem;
                font-size: 0.78rem; color: var(--text2); line-height: 1.5;">
        {mode_info[mode]}
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section-label">Query</div>', unsafe_allow_html=True)

    if mode == "5-Agent RAG Pipeline":
        question = st.text_input(
            "Your question",
            placeholder="e.g. What are the main findings of this document?",
            label_visibility="collapsed"
        )
    else:
        question = None
        st.markdown(f"""
        <div style="background: var(--surface); border: 1px solid var(--border);
                    border-radius: 6px; padding: 1rem 1.1rem; margin-bottom: 1rem;
                    font-size: 0.8rem; color: var(--text3); line-height: 1.5;
                    font-style: italic;">
            No query needed — this mode runs automatically on your uploaded document.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    ready = bool(
        uploaded_file and
        groq_key and
        tavily_key and
        (mode != "5-Agent RAG Pipeline" or question)
    )

    if not ready:
        missing = []
        if not uploaded_file: missing.append("PDF")
        if not groq_key: missing.append("Groq key")
        if not tavily_key: missing.append("Tavily key")
        if mode == "5-Agent RAG Pipeline" and not question: missing.append("question")
        st.markdown(f"""
        <div style="font-size: 0.72rem; color: var(--text3); margin-bottom: 0.5rem;">
            Waiting for: {', '.join(missing)}
        </div>
        """, unsafe_allow_html=True)

    run_btn = st.button("⬡ Run Agents", disabled=not ready)

if run_btn and ready:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_tavily import TavilySearch
    from crewai import Agent, Task, Crew
    from crewai.tools import tool
    from crewai.llm import LLM

    os.environ["GROQ_API_KEY"] = groq_key
    os.environ["TAVILY_API_KEY"] = tavily_key

    result_placeholder = st.empty()

    with st.spinner("Building knowledge base from PDF..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(uploaded_file.getvalue())
            tmp_path = f.name

        loader = PyPDFLoader(tmp_path)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        vectorstore = Chroma.from_documents(chunks, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        tavily = TavilySearch(k=3, tavily_api_key=tavily_key)

        @tool
        def search_document(question: str) -> str:
            """Search the uploaded PDF document for information relevant to the question."""
            docs = retriever.invoke(question)
            return "\n\n".join([d.page_content for d in docs])

        @tool
        def search_web(question: str) -> str:
            """Search the web for current, up-to-date information not found in the document."""
            return str(tavily.invoke(question))

        @tool
        def route_question(question: str) -> str:
            """Routes a question to either vectorstore or web_search."""
            keywords = ["document", "pdf", "text", "paper", "article",
                        "author", "according to", "mentioned", "states", "describes"]
            if any(k in question.lower() for k in keywords):
                return 'vectorstore'
            return 'web_search'

        llm = LLM(
            model="groq/llama-3.3-70b-versatile",
            max_tokens=400,
            temperature=0.1,
        )

    if mode == "5-Agent RAG Pipeline":
        with st.spinner("5 agents are working on your question..."):

            Router_Agent = Agent(
                role='Query Router',
                goal='Determine the best source to answer the user question',
                backstory="You decide whether questions are best answered using the uploaded document or by searching the web.",
                verbose=False, allow_delegation=False, llm=llm, tools=[route_question],
            )
            Retriever_Agent = Agent(
                role='Information Retriever',
                goal='Retrieve the most relevant information to answer the question',
                backstory="You retrieve information from documents or the web depending on the router decision.",
                verbose=False, allow_delegation=False, llm=llm, tools=[search_document, search_web],
            )
            Grader_agent = Agent(
                role='Relevance Grader',
                goal='Assess whether retrieved information is relevant',
                backstory="You evaluate whether retrieved content answers the question.",
                verbose=False, allow_delegation=False, llm=llm,
            )
            hallucination_grader = Agent(
                role='Hallucination Grader',
                goal='Verify the answer is grounded in retrieved facts',
                backstory="You fact-check answers against retrieved source material.",
                verbose=False, allow_delegation=False, llm=llm,
            )
            answer_grader = Agent(
                role='Answer Synthesiser',
                goal='Produce a final accurate answer',
                backstory="You produce clear, well-structured final answers.",
                verbose=False, allow_delegation=False, llm=llm, tools=[search_web],
            )

            router_task = Task(
                description=(f"Analyse: {question}\nUse route_question tool.\nReturn ONLY 'vectorstore' or 'websearch'."),
                expected_output="A single word: 'vectorstore' or 'websearch'.",
                agent=Router_Agent, tools=[route_question],
            )
            retriever_task = Task(
                description=(f"Retrieve info for: {question}\nIf 'vectorstore': use search_document.\nIf 'websearch': use search_web."),
                expected_output="A factual 3-5 sentence summary.",
                agent=Retriever_Agent, context=[router_task],
            )
            grader_task = Task(
                description=f"Is the retrieved content relevant to: {question}?",
                expected_output="Only 'yes' or 'no'.",
                agent=Grader_agent, context=[retriever_task],
            )
            hallucination_task = Task(
                description=f"Are all claims supported by sources for: {question}?",
                expected_output="Only 'yes' or 'no'.",
                agent=hallucination_grader, context=[grader_task],
            )
            answer_task = Task(
                description=(f"Give the final answer to: {question}\nIf hallucination check passed, summarise clearly. Otherwise use search_web."),
                expected_output="Clear, structured answer. End with 'Source: document' or 'Source: web search'.",
                context=[router_task, retriever_task, grader_task, hallucination_task],
                agent=answer_grader,
            )

            crew = Crew(
                agents=[Router_Agent, Retriever_Agent, Grader_agent, hallucination_grader, answer_grader],
                tasks=[router_task, retriever_task, grader_task, hallucination_task, answer_task],
                verbose=False,
            )
            result = crew.kickoff()
            mode_label = "5-AGENT RAG"

    elif mode == "Trend Analyst":
        with st.spinner("Trend Analyst is searching the web..."):

            trend_agent = Agent(
                role="Trend Analyst",
                goal="Summarise the latest news and trends related to the topic of the uploaded document",
                backstory="You are an expert analyst who searches the web for the latest developments on any given topic and distills the most important recent trends into a clear, concise summary.",
                verbose=False, allow_delegation=False, llm=llm, tools=[search_web],
            )
            trend_task = Task(
                description="Search the web and summarise the 3 most important recent trends related to the topic of the uploaded document.",
                expected_output="A clear bullet-point summary of 3 recent trends with sources.",
                agent=trend_agent,
            )
            crew = Crew(agents=[trend_agent], tasks=[trend_task], verbose=False)
            result = crew.kickoff()
            mode_label = "TREND ANALYST"

    elif mode == "Report Generator":
        with st.spinner("Report Generator is analysing your document..."):

            report_agent = Agent(
                role="Report Generator",
                goal="Collect insights from the uploaded document and generate a structured report",
                backstory="You are an expert analyst who reads uploaded documents and produces clear, structured reports summarising the key findings, challenges, and recommendations.",
                verbose=False, allow_delegation=False, llm=llm, tools=[search_document],
            )
            report_task = Task(
                description=(
                    "Using the search_document tool, search the uploaded document for information on: "
                    "1. The main topic and purpose of the document "
                    "2. Key findings or results presented "
                    "3. Challenges or limitations discussed "
                    "Then produce a structured report with sections for each topic."
                ),
                expected_output=(
                    "A structured report with three sections: "
                    "1. Document Overview "
                    "2. Key Findings "
                    "3. Challenges and Limitations. "
                    "Each section should include key findings and statistics from the document."
                ),
                agent=report_agent,
            )
            crew = Crew(agents=[report_agent], tasks=[report_task], verbose=False)
            result = crew.kickoff()
            mode_label = "REPORT GENERATOR"

    os.unlink(tmp_path)

    st.markdown(f"""
    <div class="answer-box">
        <div class="answer-header">
            <div class="answer-header-label">⬡ Agent Response</div>
            <div class="answer-badge">{mode_label}</div>
        </div>
        {str(result).replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)

    st.success("Done! Agents completed successfully.")