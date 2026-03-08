import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

docs_folder = "docs"

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []

for file in os.listdir(docs_folder):

    if file.endswith(".txt"):

        path = os.path.join(docs_folder, file)

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

            chunks = content.split("\n")

            texts.extend(chunks)

embeddings = model.encode(texts)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, "vector_db.index")

with open("texts.pkl", "wb") as f:
    pickle.dump(texts, f)

print("Vector database created.")