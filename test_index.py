import faiss
import pickle
from sentence_transformers import SentenceTransformer

INDEX_FILE = "faiss.index"
METADATA_FILE = "metadata.pkl"
MODEL_NAME = "intfloat/e5-base-v2"
TOP_K = 3

def load_index_and_metadata():
    index = faiss.read_index(INDEX_FILE)
    with open(METADATA_FILE, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def search(query, index, metadata, model, top_k=TOP_K):
    q_emb = model.encode([query], convert_to_tensor=True).cpu().numpy()
    distances, indices = index.search(q_emb, top_k)
    results = []
    for dist, idx in zip(distances[0], indices[0]):
        fname, chunk_text = metadata[idx]
        results.append({
            "filename": fname,
            "chunk": chunk_text,
            "distance": float(dist)
        })
    return results

def main():
    model = SentenceTransformer(MODEL_NAME)
    index, metadata = load_index_and_metadata()

    queries = [
        "What happened near the Outer Ring?",
        "Explain the origin and purpose of Rynor",
        "Describe the abilities of the Aegis Coloss"
    ]
    for query in queries:
        results = search(query, index, metadata, model)

        print(f"Top {TOP_K} results for query: '{query}'\n")
        for i, res in enumerate(results, 1):
            print(f"{i}. File: {res['filename']}, Distance: {res['distance']:.4f}")
            print(f"   Chunk: {res['chunk'][:200]}...")
            print("-" * 80)
        print("\n\n")

if __name__ == "__main__":
    main()
