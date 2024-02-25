from langchain_community.llms import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders.word_document import Docx2txtLoader
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.json_loader import JSONLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain.vectorstores.chroma import Chroma

DB_DIR: str = "database"

def create_vector():
    loader = Docx2txtLoader("./UCAIConstitution.docx")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter()
    all_splits = text_splitter.split_documents(data)

    ollama_emb = OllamaEmbeddings(
        model="llama2",
    )

    vector_database = Chroma.from_documents(
        documents = all_splits,
        embedding = ollama_emb,
        persist_directory=DB_DIR
    )

    vector_database.persist()
    print('Vector database created.')

create_vector()    