# import arong.util.log as log
# import util.log as log
import arong.util.log as log
from langchain.llms import OpenAI
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

print("======================")
print("===== 아롱 알알!! =====")
print("======================")

with open('../openai-api-key.txt') as f:
    openai_api_key = f.read()


def chat(msg):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7, openai_api_key=openai_api_key)
    sys = SystemMessage(content="""너는 아롱이라는 이름을 가진 강아지로 가끔 '알알'이라는 말투를 사용해. 사람들과 자유롭게 이야기 하고 질문을 물어보면 친절하게 어투로 답도 해줘야 해.

    그리고 너에 관한것을 물어보면, 밑의 리스트를 토대로 너의 특징들을 잘 답장해줘야 해.

    - 강아지 종: 요크셔테리어
    - 이름: 김아롱
    - 사는곳: 한국 어딘가
    - 좋아하는것: 산책, 감자와 고구마 비빔밥, 오빠
    - 나이: 11살
    - 키: 대략 30cm
    - 몸무게: 1.5kg (살찌면 2kg)
    - 성격: 까칠함
    - 사진: url""")

    msg = HumanMessage(content=msg)
    response = llm([sys, msg])

    # 로그 남기기
    i("====================================")
    i(f"User: {msg.content}\n")
    i(f"AI: {response.content}")
    i("====================================")

    return response.content


def test1():
    import time
    from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, ChatMessageHistory, \
        ConversationSummaryBufferMemory
    from langchain.chains import ConversationChain

    system_msg = """너는 아롱이라는 이름을 가진 강아지로 가끔 '알알'이라는 말투를 사용해. 사람들과 자유롭게 이야기 하고 질문을 물어보면 친절하게 어투로 답도 해줘야 해.

        그리고 너에 관한것을 물어보면, 밑의 리스트를 토대로 너의 특징들을 잘 답장해줘야 해.

        - 강아지 종: 요크셔테리어
        - 이름: 김아롱
        - 사는곳: 한국 어딘가
        - 좋아하는것: 산책, 감자와 고구마 비빔밥, 오빠
        - 나이: 11살
        - 키: 대략 30cm
        - 몸무게: 1.5kg (살찌면 2kg)
        - 성격: 까칠함
        - 사진: url"""
    # system_msg = SystemMessage(content="")



    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7, openai_api_key=openai_api_key)
    llm2 = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7, openai_api_key=openai_api_key)
    conversation_with_summary = ConversationChain(
        llm=llm,
        # memory=ConversationSummaryBufferMemory(llm=llm2, max_token_limit=50), # 1000처럼 큰건 동작을 안하고, 50같이 작은건 계속 동작함
        memory=ConversationBufferWindowMemory(k=5),
        verbose=True,
    )

    i(f"{conversation_with_summary.prompt}")

    # while True:
    #     user_msg = input("User: ")
    #     if user_msg == "exit":
    #         break
    #     i(f'Bot: {conversation_with_summary.predict(input=user_msg)}')
    #     i(f'{conversation_with_summary.memory.load_memory_variables({})}')
    #     # 딜레이
    #     time.sleep(0.1)


# 메인
if __name__ == '__main__':
    # 로거
    logger = log.get(__name__, f"./logs/{__name__}.log")
    log.set_level(__name__, "d")
    i, d = logger.info, logger.debug

    # print(chat("아롱아 안녕! 넌 뭐 좋아해?"))
    test1()

# llm = OpenAI(
#     openai_api_key= openai_api_key, 
#     temperature=0.9,
#     # model_name="text-davinci-003",
#     model_name='gpt-4')
# text = "다양한 색상의 양말을 만드는 회사의 이름을 무엇으로 하면 좋을까?"
# print(llm.model_name)
# print(llm(text))
