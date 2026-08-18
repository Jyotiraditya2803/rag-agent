"""Ingests data/tickets.csv into the 'tickets' Chroma collection.
Run once (or whenever the database changes): python tickest_store.py"""

import os
import sqlite3

from chromadb.utils.embedding_functions import huggingface_embedding_function

os.environ["TRANSFORMERS_VERBOSITY"] = "error"
import pandas as pd
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, embeddings

CHROMA_DIR = "chroma_store"
COLLECTION = "ticket_store"
DB_path = os.path. join("data", "tickets.db")
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


print(DB_path)
def load_tickets(DB_path:str)->list[Document]:
    conn = sqlite3.connect(DB_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets where status = 'resolved'")
    rows = cursor.fetchall()
    conn.close()


    docs = []
    for row in rows:
        content=(
            f"issue:{row['issue_type']}\n"
            f"description:{row['description']}\n"
            f"resolution:{row['resolution']}"

        )
        docs.append(Document(page_content=content,metadata={"source": "tickets", "ticket_id": row["ticket_id"], "category": str(row["category"]),"status":row["status"]},))
    return docs

def main():
      print("Loading FAQ documents ... ")
      docs = load_tickets(DB_path)
      print(f" {len(docs)} tickets entries loaded.")

      print("Loading HUGGING FACE EMBEDDING ... ")


      embeddings = HuggingFaceEmbeddings(model_name ="sentence-transformers/all-MiniLM-L6-v2")
      print("embedding loaded.")
      print(f"storing the embeddings ... in {COLLECTION}")
      vector_store = Chroma.from_documents(documents=docs, embedding=embeddings,  collection_name=COLLECTION,persist_directory=CHROMA_DIR,
)
      print(f"the {vector_store._chroma_collection.count()} data is stored successfully!")

if __name__ == "__main__":
    main()