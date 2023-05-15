import os
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA

os.environ["OPENAI_API_KEY"] = "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"

# Load all txt files in the directory
loader = DirectoryLoader('D:/IdeaProjects/document.ai/code/langchain/data/', glob='**/*.txt')
# Convert data to document objects, each file will be a document
documents = loader.load()

# Initialize loader
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
# Split the loaded documents
split_docs = text_splitter.split_documents(documents)

# Initialize openai's embeddings
embeddings = OpenAIEmbeddings()
# Store document embeddings temporarily in Chroma vector database for matching queries later
docsearch = Chroma.from_documents(split_docs, embeddings)

# Create QA object
qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch, return_source_documents=True)

# Define default response when document not found locally
default_response = "I'm sorry, I don't have information on that. Would you like me to look it up for you?"

def get_answer(query):
    # Check if document exists locally for the query
    results = qa({"query": query})
    result = results['result']
    if result != " I don't know." and result != ' 我不知道。':
        # Document found locally
        return results
    else:
        # Document not found locally, get answer from GPT model
        llm = OpenAI(model_name="text-davinci-003", max_tokens=1024)
        output = llm(prompt(query, 123))
        return output or default_response

query = "用java 写一个快排算法"

result = get_answer(query)
print(result)