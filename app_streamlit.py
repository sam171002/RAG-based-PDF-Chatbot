import os
import json
import uuid
from pathlib import Path
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# ----------------- CONFIG -----------------
SESSIONS_DIR = Path(r"your_path")
SESSIONS_DIR.mkdir(exist_ok=True)

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL = "gemini-1.5-flash"
os.environ["GOOGLE_API_KEY"] = "your_actual_api_key_here"

# ----------------- SESSION HANDLING -----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

session_file = SESSIONS_DIR / f"{st.session_state.session_id}.json"

def load_history():
    if session_file.exists():
        with open(session_file, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(session_file, "w") as f:
        json.dump(history, f)

if "history" not in st.session_state or not st.session_state.history:
    st.session_state.history = load_history()

# ----------------- STREAMLIT UI -----------------
st.set_page_config(page_title="DocuMentor RAG ChatBot", layout="wide")
st.title("DocuMentor: Interactive PDF Knowledge Bot")

uploaded_pdf = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_pdf:
    with st.spinner("Hang Tight Smarty! Processing..."):
        # Save uploaded file temporarily
        temp_pdf_path = Path(f"./temp_{uuid.uuid4().hex}.pdf")
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        loader = PyPDFLoader(str(temp_pdf_path))
        pages = loader.load_and_split()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120)
        chunks = []
        for doc in pages:
            page_num = doc.metadata.get("page", None)
            subdocs = text_splitter.split_documents([doc])
            for sd in subdocs:
                sd.metadata['page'] = page_num
                chunks.append(sd)

        embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=None
        )

        llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, api_key=os.environ["GOOGLE_API_KEY"])

        def retrieve_top_k(query, k=4):
            return vectordb.similarity_search(query, k=k)

        def answer_question(question, history, k=4):
            docs = retrieve_top_k(question, k=k)
            context = "\n\n".join([f"[page {d.metadata.get('page', '?')}] {d.page_content}" for d in docs])
            history_text = "\n".join([f"User: {h['q']}\nBot: {h['a']}" for h in history])

            prompt = f"""
            You are a helpful assistant for a PDF manual.
            Maintain conversational context.

            PREVIOUS CHAT:
            {history_text}

            CONTEXT:
            {context}

            QUESTION:
            {question}

            Answer clearly. Cite pages like [page X].
            """

            response = llm.invoke(prompt)
            return response.content, docs

        # Display past messages
        for h in st.session_state.history:
            with st.chat_message("user"):
                st.write(h["q"])
            with st.chat_message("assistant"):
                st.write(h["a"])
                if h["sources"]:
                    with st.expander("📖 Sources"):
                        for s in h["sources"]:
                            st.write(f"- Page {s.get('page')} → {s.get('page_content')[:200]}...")

        # Chat input
        if user_q := st.chat_input("Ask me something about the uploaded PDF..."):
            answer, docs = answer_question(user_q, st.session_state.history, k=4)

            sources_serializable = [{"page": d.metadata.get("page"), "page_content": d.page_content} for d in docs]
            interaction = {"q": user_q, "a": answer, "sources": sources_serializable}

            st.session_state.history.append(interaction)
            save_history(st.session_state.history)

            with st.chat_message("user"):
                st.write(user_q)
            with st.chat_message("assistant"):
                st.write(answer)
                if docs:
                    with st.expander("📖 Sources"):
                        for d in docs:
                            st.write(f"- Page {d.metadata.get('page')} → {d.page_content[:200]}...")

        # Sidebar session info + history view
        st.sidebar.write(f"Session ID: {st.session_state.session_id}")
        st.sidebar.subheader("Full Chat History")
        history_text = ""
        for h in st.session_state.history:
            history_text += f"User: {h['q']}\nBot: {h['a']}\n{'-'*30}\n"

        st.sidebar.text_area("History", value=history_text, height=400, disabled=True)

        # Cleanup temporary file
        temp_pdf_path.unlink()

else:
    st.info("📄 Please upload a PDF to start interacting with your smart chatbot.")
