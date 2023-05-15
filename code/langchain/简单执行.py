from langchain.llms import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "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"

llm = OpenAI(model_name="text-davinci-003", max_tokens=1024)
output = llm("你好")
print(output)