from langchain_community.llms import ollama
from test import doct
import os

llm = ollama.Ollama(model="llama2")

def list_joiner(list_to_join: list, sep: str) -> str:
    result = ""
    for element in list_to_join:
        result += (element+sep)
    return result

def splitIntoChunks(text:str, chunkSize:int):
    words = text.split(' ')
    chunks = []
    words = []
    currentChunk = []

    # The below loop goes through each word in the text and then splits it into chunks. 
    for word in words:
        currentChunk.append(word)
        if len(currentChunk) >= chunkSize:
            chunks.append(word.join(' '))
            currentChunk = []
    
    # If the last chunk is not empty is fills it with whitespaces in the middle
    if len(currentChunk) >= 0:
        chunks.append(currentChunk.join(' '))

    return chunks

print(splitIntoChunks(doct, 100))





