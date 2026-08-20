import sys
import os

from dotenv import load_dotenv

# Load variables from .env
load_dotenv()


# ============================================================
# SQLite fix for ChromaDB
# ============================================================

try:
    __import__("pysqlite3")
    sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
except ImportError:
    pass


# ============================================================
# NLTK
# ============================================================

import nltk

nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("averaged_perceptron_tagger_eng")


# ============================================================
# LangChain imports
# ============================================================

from uuid import uuid4
from pathlib import Path

from langchain_classic.chains import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings


# ============================================================
# Constants
# ============================================================

CHUNK_SIZE = 1000

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"

COLLECTION_NAME = "real_estate"

# Groq model
GROQ_MODEL = "llama-3.1-8b-instant"


# ============================================================
# Global variables
# ============================================================

llm = None
vector_store = None


# ============================================================
# Initialize Components
# ============================================================

def initialize_components():
    global llm, vector_store

    # --------------------------------------------------------
    # Initialize Groq LLM
    # --------------------------------------------------------

    if llm is None:

        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not configured. "
                "Please add GROQ_API_KEY to your .env file."
            )

        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model=GROQ_MODEL,
            temperature=0.9,
            max_tokens=500
        )

    # --------------------------------------------------------
    # Initialize Embeddings + ChromaDB
    # --------------------------------------------------------

    if vector_store is None:

        ef = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={
                "trust_remote_code": True
            }
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTORSTORE_DIR)
        )


# ============================================================
# Process URLs
# ============================================================

def process_urls(urls):
    """
    Scrape data from URLs, split the data into chunks,
    generate embeddings, and store the chunks in ChromaDB.
    """

    yield "Initializing Components"
    initialize_components()

    yield "Resetting vector store...✅"
    vector_store.reset_collection()

    yield "Loading data...✅"

    loader = UnstructuredURLLoader(
        urls=urls
    )

    data = loader.load()

    yield "Splitting text into chunks...✅"

    text_splitter = RecursiveCharacterTextSplitter(
        separators=[
            "\n\n",
            "\n",
            ".",
            " "
        ],
        chunk_size=CHUNK_SIZE
    )

    docs = text_splitter.split_documents(data)

    yield "Add chunks to vector database...✅"

    uuids = [
        str(uuid4())
        for _ in range(len(docs))
    ]

    vector_store.add_documents(
        docs,
        ids=uuids
    )

    yield "Done adding docs to vector database...✅"


# ============================================================
# Generate Answer
# ============================================================

def generate_answer(query):

    if vector_store is None:
        raise RuntimeError(
            "Vector database is not initialized."
        )

    chain = RetrievalQAWithSourcesChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever()
    )

    result = chain.invoke(
        {"question": query},
        return_only_outputs=True
    )

    sources = result.get(
        "sources",
        ""
    )

    return result["answer"], sources
