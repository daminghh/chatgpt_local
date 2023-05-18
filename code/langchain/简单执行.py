from langchain.llms import OpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
os.environ["OPENAI_API_KEY"] = ""

# llm = OpenAI(model_name="text-davinci-003", max_tokens=1024,streaming=True)
llm = OpenAI(streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0)
output = llm("你是谁？")
# print(output)