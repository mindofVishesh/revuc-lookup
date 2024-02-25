import argparse
import os
from langchain.chains import RetrievalQA
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.llms.ollama import Ollama
from langchain.prompts import PromptTemplate
from langchain.vectorstores.chroma import Chroma
from langchain.callbacks import AsyncIteratorCallbackHandler
prompt_template = """
Use the following pieces of context to answer the users question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.
The "SOURCES" part should be a reference to the source of the document from which you got your answer.
The example of your response should be:

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return prompt


def create_retrieval_qa_chain(llm, prompt, db):
    """
    Creates a Retrieval Question-Answering (QA) chain using a given language model, prompt, and database.

    This function initializes a RetrievalQA object with a specific chain type and configurations,
    and returns this QA chain. The retriever is set up to return the top 3 results (k=3).

    Args:
        llm (any): The language model to be used in the RetrievalQA.
        prompt (str): The prompt to be used in the chain type.
        db (any): The database to be used as the retriever.

    Returns:
        RetrievalQA: The initialized QA chain.
    """
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return qa_chain


def load_model(
    model_path=r"C:\Users\samar\.ollama\models\blobs\sha256-8934d96d3f08982e95922b2b7a2c626a1fe873d7c3b06e8e56d7bc0a1fef9246",
    model_type="llama2",
    max_new_tokens=512,
    temperature=0.7,
):
    """
    Load a locally downloaded model.

    Parameters:
        model_path (str): The path to the model to be loaded.
        model_type (str): The type of the model.
        max_new_tokens (int): The maximum number of new tokens for the model.
        temperature (float): The temperature parameter for the model.

    Returns:
        CTransformers: The loaded model.

    Raises:
        FileNotFoundError: If the model file does not exist.
        SomeOtherException: If the model file is corrupt.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No model file found at {model_path}")

    # Additional error handling could be added here for corrupt files, etc.

    llm = Ollama(
        base_url=model_path,
        model=model_type,
        #max_new_tokens=max_new_tokens,  # type: ignore
        temperature=temperature,  # type: ignore
    )

    return llm


def create_retrieval_qa_bot(
    model_name="llama2",
    persist_dir=r"C:\Users\samar\OneDrive\Desktop\revuc-hackathon\revuc-lookup",
    device="cpu",
):
    """
    This function creates a retrieval-based question-answering bot.

    Parameters:
        model_name (str): The name of the model to be used for embeddings.
        persist_dir (str): The directory to persist the database.
        device (str): The device to run the model on (e.g., 'cpu', 'cuda').

    Returns:
        RetrievalQA: The retrieval-based question-answering bot.

    Raises:
        FileNotFoundError: If the persist directory does not exist.
        SomeOtherException: If there is an issue with loading the embeddings or the model.
    """

    if not os.path.exists(persist_dir):
        raise FileNotFoundError(f"No directory found at {persist_dir}")

    try:
        embeddings = OllamaEmbeddings(
            model=model_name,
        )
    except Exception as e:
        raise Exception(
            f"Failed to load embeddings with model name {model_name}: {str(e)}"
        )

    db = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

    try:
        llm = load_model()  # Assuming this function exists and works as expected
    except Exception as e:
        raise Exception(f"Failed to load model: {str(e)}")

    qa_prompt = (
        set_custom_prompt()
    )  # Assuming this function exists and works as expected

    try:
        qa = create_retrieval_qa_chain(
            llm=llm, prompt=qa_prompt, db=db
        )  # Assuming this function exists and works as expected
    except Exception as e:
        raise Exception(f"Failed to create retrieval QA chain: {str(e)}")

    return qa


def retrieve_bot_answer(query):
    """
    Retrieves the answer to a given query using a QA bot.

    This function creates an instance of a QA bot, passes the query to it,
    and returns the bot's response.

    Args:
        query (str): The question to be answered by the QA bot.

    Returns:
        dict: The QA bot's response, typically a dictionary with response details.
    """
    qa_bot_instance = create_retrieval_qa_bot()
    bot_response = qa_bot_instance({"query": query})
    return bot_response

def process_query(qa_bot, query):
  response = qa_bot.acall(query)
  answer = response["result"]
  source_documents = response.get("source_documents", [])
  print(f"Answer: {answer}")
  if source_documents:
    print(f"\nSources: {source_documents}")
  else:
    print("\nNo sources found")

def main():
#   parser = argparse.ArgumentParser(description="Retrieval-based QA with CLI")
#   parser.add_argument("query", help="Summarize")
#   args = parser.parse_args()

  query = input("Hello World: ")

  qa_bot = create_retrieval_qa_bot(...)
  process_query(qa_bot, query)

if __name__ == "__main__":
  main()

# llm = load_model()
# print(retrieve_bot_answer("Summarize the document"))