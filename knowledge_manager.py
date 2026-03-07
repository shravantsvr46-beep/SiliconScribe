from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS vector database
db = FAISS.load_local(
    "vector_store",
    embeddings,
    allow_dangerous_deserialization=True
)


def get_datasheet_context(mcu, user_input):

    query = f"{mcu} {user_input}"

    docs = db.similarity_search(query, k=5)

    context = ""

    for doc in docs:
        context += doc.page_content + "\n"

    return context