import os
import ollama

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

documents = []

DOCS_PATH = "./documents"

for file in os.listdir(DOCS_PATH):

    if file.endswith(".pdf"):

        path = os.path.join(DOCS_PATH, file)

        loader = PyPDFLoader(path)

        documents.extend(loader.load())

print(f"Loaded {len(documents)} pages")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="./db"
)

print("Vector DB Ready")

while True:

    query = input("\nAsk Question: ")

    if query.lower() == "exit":
        break

    results = vectordb.similarity_search(query, k=3)

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    prompt = f"""
Answer ONLY from this context.

Context:
{context}

Question:
{query}
"""

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nANSWER:\n")

    print(response["message"]["content"])
