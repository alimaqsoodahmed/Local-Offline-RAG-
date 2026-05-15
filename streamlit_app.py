import os
import streamlit as st
import ollama

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ---------------- UI ----------------
st.set_page_config(
    page_title="Offline Personal RAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Offline Personal RAG")
st.markdown("Upload PDFs and chat with them locally using Ollama + LangChain")

# ---------------- Session State ----------------
if "vectordb" not in st.session_state:
    st.session_state.vectordb = None

if "ready" not in st.session_state:
    st.session_state.ready = False

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("Settings")
    top_k = st.slider("Top retrieved chunks", 1, 10, 3)

    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )

    build_btn = st.button("Build / Rebuild Knowledge Base", use_container_width=True)

# ---------------- Helpers ----------------
@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def save_uploaded_files(uploaded_files, folder="temp_docs"):
    os.makedirs(folder, exist_ok=True)
    paths = []
    for file in uploaded_files:
        path = os.path.join(folder, file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        paths.append(path)
    return paths

def load_pdf_docs(file_paths):
    docs = []
    for path in file_paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    return docs

def build_vectorstore(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    chunks = splitter.split_documents(docs)

    if not chunks:
        raise ValueError("No readable text found in the uploaded PDFs.")

    embedding = get_embedding_model()

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory="db"
    )

    return vectordb, len(chunks)

# ---------------- Main UI ----------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Chat with your PDFs")
    question = st.text_input("Ask a question from the uploaded documents")

with col2:
    st.subheader("Status")
    if st.session_state.ready:
        st.success("Knowledge base ready")
    else:
        st.warning("Not built yet")

# ---------------- Build KB ----------------
if build_btn:
    if not uploaded_files:
        st.error("Upload at least one PDF first.")
    else:
        try:
            with st.spinner("Saving PDFs..."):
                file_paths = save_uploaded_files(uploaded_files)

            with st.spinner("Loading PDF text..."):
                docs = load_pdf_docs(file_paths)

            st.info(f"Loaded {len(docs)} pages")

            with st.spinner("Building vector database..."):
                vectordb, chunk_count = build_vectorstore(docs)
                st.session_state.vectordb = vectordb
                st.session_state.ready = True

            st.success(f"Created {chunk_count} chunks and built the vector DB.")
        except Exception as e:
            st.error(f"Build failed: {e}")

# ---------------- Ask Question ----------------
if question:
    if st.session_state.vectordb is None:
        st.warning("First upload PDFs and click 'Build / Rebuild Knowledge Base'.")
    else:
        try:
            with st.spinner("Searching and generating answer..."):
                results = st.session_state.vectordb.similarity_search(question, k=top_k)

                context = "\n\n".join(
                    [f"[Page {doc.metadata.get('page', 'N/A')}] {doc.page_content}" for doc in results]
                )

                prompt = f"""
You are a helpful assistant.
Answer ONLY using the context below.
If the answer is not in the context, say you could not find it in the uploaded PDFs.

Context:
{context}

Question:
{question}

Answer:
"""

                response = ollama.chat(
                    model="llama3.2:1b",
                    messages=[{"role": "user", "content": prompt}]
                )

                answer = response["message"]["content"]

            st.markdown("### Answer")
            st.write(answer)

            with st.expander("Retrieved context"):
                st.text(context)

        except Exception as e:
            st.error(f"Query failed: {e}")