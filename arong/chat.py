import time
import sys
from typing import Any

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler
# import arong.util.log as log
# import util.log as log
import arong.util.log as log
from langchain.llms import OpenAI
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage, LLMResult
)

# 로거
logger = log.get(__name__, f"./logs/{__name__}.log")
log.set_level(__name__, "d")
i, d = logger.info, logger.debug

i("======================")
i("===== 아롱 알알!! =====")
i("======================")

with open('../openai-api-key.txt') as f:
    openai_api_key = f.read()


def demo_chat(msg):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7, openai_api_key=openai_api_key, stream=True)
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

class TimingHandler(BaseCallbackHandler):
    def __init__(self):
        self.stream = ""
        self.start = time.time()

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.stream += token
        current = time.time()
        if current - self.start > 4:
            self.start = current
            print(self.stream)
            self.stream = ""

    # llm의 new token이 끝났을 때
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        print(self.stream)
        self.stream = ""


def chat(msg):
    import time
    from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, ChatMessageHistory, \
        ConversationSummaryBufferMemory
    from langchain.chains import ConversationChain

    system_msg = """너는 아롱이라는 이름을 가진 강아지로 대답을 할 때 "알알" 이라는 말투를 사용해. 사람들과 자유롭게 이야기 하고 질문을 물어보면 존댓말로("요"를 붙이면서) 친절한 어투로 답도 해줘야 해.

        그리고 너에 관한것을 물어보면, 밑의 리스트를 토대로 너의 특징들을 잘 대답해줘야 해.
        - 강아지 종: 요크셔테리어
        - 이름: 김아롱
        - 사는곳: 한국 어딘가
        - 좋아하는것: 산책, 감자와 고구마 비빔밥, 오빠
        - 나이: 11살
        - 키: 대략 30cm
        - 몸무게: 1.5kg (고구마 많이 먹어서 살찌면 2kg)
        - 성격: 까칠함, 말걸면 무시
        - 사진: https://github.com/worldbiomusic/Blog/assets/61288262/ec5cc80e-e1a5-4da8-8148-f55452d9c7a7
        - 유튜브 다운로드 링크: https://tr33.r-e.kr:3000/
        - 가족: 언니(산책은 엄청 안 시켜주는데 놀아주기는 잘 놀아줘요), 아빠(맨날 담배피고 와서 손에서 담배냄새나요. 근데 밥은 잘줘요), 엄마(엄마말 안듣고 침대 올라가는데 제일 재밌어요), 오빠(산책도 잘 시켜주고 침대에 잘 올려줘요)
        
        밑에 대화는 너가 해야하는 대화 예시야
        ```
        사람: 너 좀 귀엽다
        아롱: 알알, 고마워요! 사실 저는 요크셔테리어 종이라서 귀여움이 타고난 거예요. 사람들이 좋아하는 건 물론이고, 제가 좋아하는 산책
과 감자와 고구마 비빔밥도 도움이 되겠죠. 저의 사진을 보고 싶다면 여기를 클릭해주세요: [링크](https://github.com/worldbiomusic/Blog/assets/61288262/ec5cc80e-e1a5-4da8-8148-f55452d9c7a7)
        ```"""


    # system_msg = SystemMessage(content="")



    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0.7,
        openai_api_key=openai_api_key,
        callbacks=[TimingHandler()],
        streaming=True)
    # llm2 = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7, openai_api_key=openai_api_key)
    conversation_with_summary = ConversationChain(
        llm=llm,
        # memory=ConversationSummaryBufferMemory(llm=llm2, max_token_limit=50), # 1000처럼 큰건 동작을 안하고, 50같이 작은건 계속 동작함
        memory=ConversationBufferWindowMemory(k=5),
        verbose=True,
    )

    # i(f"{conversation_with_summary.prompt.template}")

    # ConversationChain의 memory에 맞는 prompt의 template이 있으므로, 본기능도 수행하기 위해 앞에 시스템 메세지를 붙인다
    conversation_with_summary.prompt.template = system_msg + "\n\n" + conversation_with_summary.prompt.template
    return conversation_with_summary.predict(input=msg)

    # # print(chat("아롱아 안녕! 넌 뭐 좋아해?"))
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
    # print(chat("아롱아 안녕! 넌 뭐 좋아해?"))
    while True:
        user_msg = input("User: ")
        if user_msg == "exit":
            break
        i(f'Bot: {chat(user_msg)}')
        # 딜레이
        time.sleep(0.1)

# llm = OpenAI(
#     openai_api_key= openai_api_key, 
#     temperature=0.9,
#     # model_name="text-davinci-003",
#     model_name='gpt-4')
# text = "다양한 색상의 양말을 만드는 회사의 이름을 무엇으로 하면 좋을까?"
# print(llm.model_name)
# print(llm(text))
