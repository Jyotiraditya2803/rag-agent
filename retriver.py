"""
Builds a merged retriever across all three Chroma collections:
  - faq     : FAQ entries (no chunking — 1 row = 1 doc)
  - tickets : resolved support tickets (no chunking — 1 ticket = 1 doc)
  - guides  : PDF guide chunks (RecursiveCharacterTextSplitter applied at ingest)
"""
import chroma
#from chromadb.utils.embedding_functions import huggingface_embedding_function
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.runnables import RunnableLambda
from langchain_core.documents import Document
from pandas.core.window.doc import kwargs_scipy

CHROMA_DIR  = "chroma_store"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def bulid_retriver(faq_k:int =3,ticket:int =3,pdf:int =3,)->RunnableLambda:
     embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
     faq_store= Chroma(
          collection_name="faq",
          embedding_function= embeddings,
          persist_directory=CHROMA_DIR,
     )
     ticket_store= Chroma(
          collection_name="tickets",
          embedding_function =embeddings,
          persist_directory=CHROMA_DIR,
     )
     pdf_store = Chroma(
          collection_name="guides",
          embedding_function=embeddings,
          persist_directory=CHROMA_DIR,
     )

     faq_retriever =faq_store.as_retriever(search_kwargs={"k":faq_k})
     ticket_retriever = ticket_store.as_retriever(search_kwargs={"k":ticket})
     pdf_retriever = pdf_store.as_retriever(search_kwargs={"k":pdf})

     def retriver(query:str)->list[Document]:
       return(
          faq_retriever.invoke(query)
          + ticket_retriever.invoke(query)
          + pdf_retriever.invoke(query)
     )
     return RunnableLambda(retriver)