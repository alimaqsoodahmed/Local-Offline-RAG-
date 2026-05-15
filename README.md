# 📚 Offline Personal RAG

A fully offline Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about them locally using:

- Streamlit
- Ollama
- Llama 3.2:1b
- LangChain
- ChromaDB
- Sentence Transformers

The system runs completely offline after model installation and keeps all documents private on the local machine.

---

# 🚀 Features

✅ Upload personal PDF documents  
✅ Build a local vector database  
✅ Ask questions from uploaded documents  
✅ Fully offline after setup  
✅ Local LLM inference using Ollama  
✅ Simple Streamlit web interface  
✅ Private and secure document querying  

---

🖼️ Screenshots
Main Interface
   Home

  🎥 Demo Video
     Working Demo Video

Add your screen recording link here after uploading to YouTube or LinkedIn.
---
# 🧠 Architecture

The application follows a Retrieval-Augmented Generation (RAG) pipeline.

```text
PDF Upload
    ↓
PyPDFLoader
    ↓
Text Chunking
    ↓
Sentence Embeddings
    ↓
Chroma Vector Database
    ↓
Similarity Search
    ↓
Retrieved Context
    ↓
Ollama (Llama 3.2:1b)
    ↓
Generated Answer
```

---

# ⚙️ How It Works

## 1. Upload PDFs
The user uploads one or more PDF files through the Streamlit interface.

## 2. PDF Text Extraction
`PyPDFLoader` extracts text page-by-page from the documents.

## 3. Text Chunking
The text is split into smaller chunks using:

- chunk size = 500
- overlap = 100

This improves retrieval quality.

## 4. Embedding Generation
Each chunk is converted into vector embeddings using:

```python
sentence-transformers/all-MiniLM-L6-v2
```

## 5. Vector Storage
Embeddings are stored locally using ChromaDB.

## 6. Similarity Search
When a question is asked:

- the query is converted into embeddings
- Chroma retrieves the most relevant chunks

## 7. Response Generation
The retrieved chunks are passed to:

```text
llama3.2:1b
```

running locally through Ollama.

The model generates the final answer using only the retrieved context.

---

# 📂 Project Structure

```text
offline-rag/
│
├── app.py
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── documents/
├── db/
├── temp_docs/
│
└── venv/
```

---

# 🖥️ Installation Guide

## 1. Clone Repository

```powershell
git clone https://github.com/YOUR_USERNAME/offline-rag.git
cd offline-rag
```

---

## 2. Create Virtual Environment

```powershell
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

---

## 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🦙 Install Ollama

Download and install Ollama:

https://ollama.com/download

---

# 📥 Pull the Llama Model

```powershell
ollama pull llama3.2:1b
```

---

# ▶️ Running the Application

## Terminal 1 — Start Ollama

```powershell
ollama run llama3.2:1b
```

Keep this terminal open.

---

## Terminal 2 — Start Streamlit

```powershell
streamlit run streamlit_app.py
```

---

# 🌐 Using the App

1. Upload PDF files
2. Click:

```text
Build / Rebuild Knowledge Base
```

3. Wait until the vector database is created
4. Ask questions about the uploaded documents
5. Receive answers generated locally

---

# 🛠️ Development Mode

## CLI Version

You can also use the terminal-based version:

```powershell
python app.py
```

This is useful for debugging and testing retrieval.

---

# 🔒 Privacy

This application runs completely locally:

- No cloud APIs
- No external document storage
- No internet required after setup
- All PDFs remain on the user's machine

---

# 📦 Technologies Used

- Python
- Streamlit
- Ollama
- LangChain
- ChromaDB
- Sentence Transformers
- PyPDF
- Llama 3.2:1b

---

# 🧩 Future Improvements

Potential upgrades:

- Chat history memory
- Multi-document indexing
- Mobile frontend
- Docker deployment
- Hybrid search
- Better chunk ranking
- Voice interaction
- Multi-modal support
- Android APK version

---

# 👨‍💻 Author

Ali

MS Artificial Intelligence  
Air University Islamabad

---

# 📄 License

This project is open-source and available for educational and research purposes.