from langchain_community.llms import Ollama

llm = Ollama(model=r"C:\Users\samar\.ollama\models\blobs\sha256-8934d96d3f08982e95922b2b7a2c626a1fe873d7c3b06e8e56d7bc0a1fef9246")

llm.invoke("Tell me a joke")