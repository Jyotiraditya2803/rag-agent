"""Ingests data/faq.csv into the 'faq' Chroma collection.
Run once (or whenever the CSV changes): python ingest_faq.py"""

import os

from chromadb.utils.embedding_functions import huggingface_embedding_function

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, embeddings

CHROMA_DIR = "chroma_store"
COLLECTION = "faq"
CSV_PATH = os.path. join("data", "faq.csv")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_faq_documents(csv_path: str) -> list[Document]:
    df = pd.read_csv(csv_path)
    docs = []
    for _, row in df.iterrows():
        content = f"Q: {row['question']}\nA: {row['answer']}"
        docs.append(Document(
            page_content=content,
            metadata={"source": "faq", "category": row["category"], "faq_id": str(row["id"])},
        ))
    return docs

def main():
      print("Loading FAQ documents ... ")
      docs = load_faq_documents (CSV_PATH)
      print(f" {len(docs)} FAQ entries loaded.")

      print("Loading HUGGING FACE EMBEDDING ... ")


      embeddings = HuggingFaceEmbeddings(model_name ="sentence-transformers/all-MiniLM-L6-v2")
      print("embedding loaded.")
      print(f"storing the embeddings ... in {COLLECTION}")
      vector_store = Chroma.from_documents(documents=docs, embedding=embeddings,  collection_name=COLLECTION,persist_directory=CHROMA_DIR,
)
      print(f"the {vector_store._chroma_collection.count()} data is stored successfully!")


if __name__ == "__main__":
    main()
