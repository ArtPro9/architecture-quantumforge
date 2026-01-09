import os
import time
import pickle
import torch
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIR = "knowledge_base/prepared"
INDEX_FILE = "faiss.index"
METADATA_FILE = "metadata.pkl"
MODEL_NAME = "intfloat/e5-base-v2"
BATCH_SIZE = 10
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 500


def load_documents(directory):
    """Загружает все .txt файлы из директории."""
    docs = []
    filenames = []

    for fname in os.listdir(directory):
        if fname.endswith(".txt"):
            path = os.path.join(directory, fname)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                if text.strip():
                    docs.append(text)
                    filenames.append(fname)
    return docs, filenames


def chunk_documents(docs, filenames, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    """Разбивает все документы на чанки с помощью RecursiveCharacterTextSplitter."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = []
    chunk_metadata = []

    for fname, text in zip(filenames, docs):
        text_chunks = splitter.split_text(text)
        for chunk in text_chunks:
            chunks.append(chunk)
            chunk_metadata.append((fname, chunk))

    return chunks, chunk_metadata


def generate_embeddings(model, texts, batch_size=BATCH_SIZE):
    """Создаёт эмбеддинги для списка текстов с использованием батчей."""
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.encode(
            batch,
            convert_to_tensor=True,
            show_progress_bar=True
        )
        embeddings.append(batch_embeddings.cpu().numpy())
    return np.vstack(embeddings)


def build_faiss_index(embeddings):
    """Создаёт FAISS индекс и добавляет эмбеддинги."""
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index


def save_index(index, metadata, index_file=INDEX_FILE, metadata_file=METADATA_FILE):
    """Сохраняет индекс FAISS и метаданные."""
    faiss.write_index(index, index_file)
    with open(metadata_file, "wb") as f:
        pickle.dump(metadata, f)


def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Loading model {MODEL_NAME} on {device}...")
    model = SentenceTransformer(MODEL_NAME, device=device)

    print(f"Loading documents from '{DOCS_DIR}'...")
    docs, filenames = load_documents(DOCS_DIR)
    if not docs:
        print("No documents found. Exiting.")
        return
    print(f"Loaded {len(docs)} documents.")

    print("Splitting documents into chunks...")
    start_time = time.time()
    chunks, chunk_metadata = chunk_documents(docs, filenames)
    elapsed = time.time() - start_time
    print(f"Created {len(chunks)} chunks in {elapsed:.2f} seconds.")

    print("Generating embeddings...")
    start_time = time.time()
    embeddings = generate_embeddings(model, chunks)
    elapsed = time.time() - start_time
    print(f"Embeddings generated in {elapsed:.2f} seconds. Shape: {embeddings.shape}")

    print("Building FAISS index...")
    start_time = time.time()
    index = build_faiss_index(embeddings)
    elapsed = time.time() - start_time
    print(f"Index built in {elapsed:.2f} seconds with {index.ntotal} vectors.")

    print(f"Saving index to '{INDEX_FILE}' and metadata to '{METADATA_FILE}'...")
    save_index(index, chunk_metadata)
    print("Done.")


if __name__ == "__main__":
    main()
