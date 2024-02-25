# QueryPages - Conversational Search Framework

QueryPages provides a **framework** for building conversational search interfaces powered by AI. 

It includes both the core framework for integrating **semantic search** and **question answering** into chatbots, as well as a demo to showcase capabilities.

## Framework

The key components of the framework include:

- **Document ingestion** - Tools for ingesting various file formats like PDFs, DOCs, CSVsm and JSONs 
- **Embedding** - Embed documents for semantic search using SOTA models like LLaMA2
- **Indexing** - Vector database for approximate nearest neighbor search  
- **RetrievalQA** - Out-of-the-box conversational search chain 

Together these components handle:

- Understanding **natural language** queries
- Finding relevant documents 
- Extracting answers

The framework is designed to be **extensible** - additional data sources can be easily integrated by writing loaders and embedding documents.

## Demo

We have built a simple chatbot GUI demo that showcases the capabilities of this framework. Users can:  

- Have a natural language conversation
- Get relevant answers extracted from documents

The demo serves as a reference to help adopters integrate the framework into their own applications.

## Getting Started 

To try out the demo:

```bash
python index.py
```

And to leverage the framework:

```python
from querypages import DocumentSearch

search = DocumentSearch()
search.index_documents(/my_documents) 
answer = search.query("What is the capital of France?")
```
## Tech Stack
### Programming Languages

- **Python** - Used for all logic and scripts

### Frameworks and Libraries

- **Taipy** - GUI framework to build the frontend interface
- **LangChain** - Library for conversational AI and building chatbots
- **langchain_community** - Additional LangChain components from the open source community
- **asyncio** - For running asynchronous logic

## AI Models

- **LLaMA** - Cross-lingual language model used for text embeddings and question answering
- **Ollama** - LLaMA model implementation from Anthropic used in LangChain

## Vector Store

- **Chroma** - Approximate nearest neighbor index from LangChain Community for semantic search

## Document Loaders

- **Docx2txtLoader** - Extract text from .docx files
- **PyPDFLoader** - Extract text from PDFs 
- **JSONLoader** - Load JSON file contents 
- **CSVLoader** - Load CSV data

## App Server 

The GUI is served through:

- **Taipy** - Includes a development web server
