from langchain.llms import OpenAI
import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ChatVectorDBChain, ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

os.environ["OPENAI_API_KEY"] = "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"

# 加载 youtube 频道
loader = DirectoryLoader('D:/IdeaProjects/document.ai/code/langchain/data/', glob='**/*.txt')
# 将数据转成 document
documents = loader.load()

# 初始化文本分割器
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=0
)

# 分割 youtube documents
documents = text_splitter.split_documents(documents)

# 初始化 openai embeddings
embeddings = OpenAIEmbeddings()

# 将数据存入向量存储
vector_store = Chroma.from_documents(documents, embeddings)
# 通过向量存储初始化检索器
retriever = vector_store.as_retriever()
system_template = """
Use the following context to answer the user's question.
If you don't know the answer, say you don't, don't try to make it up. And answer in Chinese.
-----------
{context}
-----------
{chat_history}
"""

# 构建初始 messages 列表，这里可以理解为是 openai 传入的 messages 参数
messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template('{question}')
]

# 初始化 prompt 对象
prompt = ChatPromptTemplate.from_messages(messages)


# 初始化问答链
qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.1,max_tokens=1024),retriever)


chat_history = []
while True:
    question = input('问题：')
    # 开始发送问题 chat_history 为必须参数,用于存储对话历史
    result = qa({'question': question, 'chat_history': chat_history})
    chat_history.append((question, result['answer']))
    print(result['answer'])