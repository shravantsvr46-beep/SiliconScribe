import faiss
import pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("vector_db.index")

with open("texts.pkl", "rb") as f:
    texts = pickle.load(f)


def retrieve_context(query, top_k=3):

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    context = ""

    for i in indices[0]:
        context += texts[i] + "\n"

    return context