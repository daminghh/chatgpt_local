from langchain.llms import OpenAI
from flask import Flask
from flask import render_template
from flask import request
from qdrant_client import QdrantClient
import openai
import os

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"

def prompt(question, answers):
    demo_q = 'PA1怎么样'
    demo_a = 'PA1是一款时尚、舒适、百搭的裤子，适合多种场合穿着，如日常街拍、聚会、约会等。'
    system = '你是一个小着客服,可能有些回答不是你回答的，但是历史记录是记录的你回答的，你不用理会。最后，输出的时候注意格式，严格按照我的格式输出，下面是小着文案风格，请记住它。多留空白、空行。' \
             '小着，\n\n干净利落的高级时装。\n\n是\n\n上班穿的，下班也好穿。\n\n是 不收腰的。\n\n是 不紧绷的。\n\n是 没有藏蓝色的。\n\n是 没有廉价塑料纽扣的。\n\n是赞颂创造一点新东西，\n\n改变一点点世界的 人们。'
    q = ''
    q += question + '"'
    # 带有索引的格式
    res = [
        {'role': 'system', 'content': system},
        {'role': 'user', 'content': demo_q},
        {'role': 'assistant', 'content': demo_a},
        {'role': 'user', 'content': q},
    ]
    return res


completion = openai.ChatCompletion.create(
    temperature=0.7,
    model="gpt-3.5-turbo",
    messages=prompt("可以更好的说一下吗？,注意用小着的格式输出", ""),
)
print("completion:",completion.choices[0].message.content)