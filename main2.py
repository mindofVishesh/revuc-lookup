import asyncio
import os
from langchain import hub
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import RetrievalQA
from langchain.prompts import StringPromptTemplate, BasePromptTemplate

'''
class MyPromptTemplate(StringPromptTemplate, BasePromptTemplate):
    prompt_template = """
    Use the following pieces of context to answer the users question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer 123.
    ALWAYS return a "SOURCES" part in your answer.
    The "SOURCES" part should be a reference to the source of the document from which you got your answer.
    The example of your response should be:

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
"""

prompt_template = MyPromptTemplate(template=prompt_template, input_variables=["context", "question"])
'''
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
        #chain_type_kwargs={"prompt": prompt_template},
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
    print("Hi, Welcome to Chat With Documents using Ollama (mistral model) and LangChain.")
    user_session = {"chain": chain}
    return user_session

def main(user_session, user_input):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    chain = user_session.get("chain")
    res = loop.run_until_complete(chain.acall(user_input))
    answer = res["result"]

    source_documents = res["source_documents"]
    '''
    if source_documents:
        print(f"Sources: {', '.join([f'source_{i}' for i in range(len(source_documents))])}")
    else:
        print("No sources found")
    '''
    #print(answer)

# Example usage
user_session = start()

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    main(user_session, user_input)