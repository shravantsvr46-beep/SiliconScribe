import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


def get_datasheet_context(mcu_name, query, api_key):

    pdf_path = os.path.join("docs", f"{mcu_name.lower()}_manual.pdf")

    if not os.path.exists(pdf_path):
        return "No datasheet available. Use general microcontroller knowledge."

    try:

        loader = PyPDFLoader(pdf_path)
        docs = loader.load_and_split()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(docs)

        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )

        vectorstore = FAISS.from_documents(chunks, embeddings)

        results = vectorstore.similarity_search(query, k=3)

        return "\n".join([r.page_content for r in results])

    except Exception as e:
        return f"Error reading datasheet: {e}"