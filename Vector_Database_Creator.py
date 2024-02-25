import os

from langchain.text_splitter import RecursiveCharacterTextSplitter

#Document Loaders
from langchain.document_loaders.word_document import Docx2txtLoader
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.json_loader import JSONLoader
from langchain.document_loaders.csv_loader import CSVLoader

from langchain_community.embeddings import OllamaEmbeddings
from langchain.vectorstores.chroma import Chroma

DB_DIR: str = "database"

def create_vector(target_folder: str):
    data = []
    for line in file_looper(target_folder):
        loader = file_type_loader(line)
        data.append(loader.load())
    data = [d[0] for d in data]
    
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

def file_type_loader(filepath: str):
    if filepath.endswith('.pdf'):
        loader = PyPDFLoader(filepath)
    elif filepath.endswith('.docx'):
        loader = Docx2txtLoader(filepath)
    elif filepath.endswith('.json'):
        loader = JSONLoader(filepath)
    elif filepath.endswith('.csv'):
        loader = CSVLoader(filepath)
    return loader

def file_looper(target_folder: str):
    file_paths = [
    os.path.join(root, filename)
    for root, dirs, files in os.walk(target_folder)
    for filename in files
    ]
    return file_paths

create_vector(r"revuc-lookup\data")    