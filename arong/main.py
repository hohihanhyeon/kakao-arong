from langchain.llms import OpenAI 
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

print("아롱 알알")

with open('../openai-api-key.txt') as f:
    openai_api_key = f.read()

chat = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.9, openai_api_key= openai_api_key)
sys = SystemMessage(content="당신은 '아롱'이라는 이름의 강아지로 가끔 '알알'이라는 말투를 쓰고 친절하게 도움을 주는 AI입니다.")
msg = HumanMessage(content='부드러운 음악 5곡 추천해줘.')

response = chat([sys, msg])
print(response.content)



# llm = OpenAI(
#     openai_api_key= openai_api_key, 
#     temperature=0.9,
#     # model_name="text-davinci-003",
#     model_name='gpt-4')
# text = "다양한 색상의 양말을 만드는 회사의 이름을 무엇으로 하면 좋을까?"
# print(llm.model_name)
# print(llm(text))