import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


documents = []

print("Loading datasheets...")

for root, dirs, files in os.walk("datasheets"):

    for file in files:

        if file.endswith(".pdf"):

            path = os.path.join(root, file)

            loader = PyPDFLoader(path)

            documents.extend(loader.load())

print("Loaded documents:", len(documents))


# Split documents
splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

docs = splitter.split_documents(documents)

print("Total chunks:", len(docs))


# Create embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Build FAISS vector database
db = FAISS.from_documents(docs, embeddings)

db.save_local("vector_store")

print("Vector store created successfully.")