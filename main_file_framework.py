import asyncio
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA


def load_model():
    llm = Ollama(
        model="llama2",
        verbose=True,
        callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
    )
    return llm


def retrieval_qa_chain(llm, vectorstore):
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
    )
    return qa_chain

def qa_bot():
    llm = load_model()
    DB_PATH = "database"
    vectorstore = Chroma(
        persist_directory=DB_PATH, embedding_function=OllamaEmbeddings(model="llama2")
    )

    qa = retrieval_qa_chain(llm, vectorstore)
    return qa


def start():
    """
    Initializes the bot when a new chat starts.

    This function creates a new instance of the retrieval QA bot,
    sends a welcome message, and stores the bot instance in the user's session.
    """
    chain = qa_bot()
    print("Starting the bot...")
    print("Hi, Welcome to Chat With Documents using Ollama (llama2 model) and LangChain.")
    user_session = {"chain": chain}
    return user_session

user_session = start()

def main(user_input):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    chain = user_session.get("chain")
    res = loop.run_until_complete(chain.ainvoke(user_input))
    print(res)
    answer = res["result"]
    return answer

# Example usage
while True:
   user_input = input("You: ")
   main(user_input)


