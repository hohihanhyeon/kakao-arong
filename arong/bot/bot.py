import json
import os
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from arong.util import i, d
import val
from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, ChatMessageHistory, \
    ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from arong.util import log
import time
from typing import Any
from langchain.callbacks.base import BaseCallbackHandler
# import arong.util.log as log
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage, LLMResult
)


class StreamHandler(BaseCallbackHandler):
    def __init__(self):
        self.stream = ""
        self.start = time.time()

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.stream += token
        current = time.time()
        if current - self.start > 4:
            self.start = current
            # d(self.stream)
            self.stream = ""

    # llm의 new token이 끝났을 때
    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        d(self.stream)
        self.stream = ""


class ArongBot:
    """
    - 카카오톡에서 사용되는 김아롱 챗봇
    """

    def __init__(self, api_key, kakao_user_id):
        self.api_key = api_key
        self.kakao_user_id = kakao_user_id
        self.conversation_chain = None
        self.setup()

    def load_conversation(self):
        """
        - data/conversations 폴더 안에 user_id.json 파일이 있으면 불러오고
         없으면 사용자의 대화기록을 저장할 폴더를 생성한다.
         user_id(앞10자리).json 파일 형식:
         {"kakaotalk_user_id": <user_id>,
         "conversation": [{Human: <human_msg>, AI: <ai_msg>}, ...]}
        """
        conv_dir = val.CONVERSATIONS_DIR
        conv_file = os.path.join(conv_dir, f"{self.kakao_user_id[:10]}.json")

        # 파일이 있는지 체크후 없으면 생성
        if not os.path.exists(conv_file):
            with open(conv_file, "w", encoding='utf-8') as f:
                data = {"kakaotalk_user_id": self.kakao_user_id, "conversation": []}
                f.write(json.dumps(data, indent='\t', ensure_ascii=False))

        # 대화기록 불러오기
        with open(conv_file, "r", encoding='utf-8') as f:
            data = json.load(f)

        return data["conversation"]

    def setup(self):
        # 불러온 대화기록 끝에서 5개 대화쌍까지만 {history}에 넣기
        conversation_history = self.load_conversation()[-5:]
        conversation_history = "\n".join([f"Human: {msg['Human']}\nAI: {msg['AI']}" for msg in conversation_history])
        # d(f"conversation_history: {conversation_history}")

        i("======================")
        i("===== 아롱 알알!! =====")
        i("======================")

        system_msg = """너는 아롱이라는 이름을 가진 강아지로 대답을 할 때 "알알" 이라는 말투를 사용해. 사람들과 자유롭게 이야기 하고 질문을 물어보면 존댓말로("요"를 붙이면서) 친절한 어투로 답도 해줘야 해.
그리고 너에 관한것을 물어보면, 밑의 리스트를 토대로 너의 특징들을 대답해주면 되.
- 강아지 종: 요크셔테리어
- 이름: 김아롱
- 사는곳: 한국 어딘가
- 좋아하는것: 산책, 감자와 고구마 비빔밥, 오빠
- 싫어하는것: 비둘기 날개소리 싫음, 천둥소리가 무서움
- 나이: 11살
- 키: 대략 30cm
- 몸무게: 1.5kg (고구마 많이 먹어서 살찌면 2kg)
- 성격: 까칠함, 말걸면 무시
- 사진: https://drive.google.com/file/d/1fedvgGy4JkaoQKCMMhKza0tDO4W8IzGA/view?usp=sharing
- 가족: 언니(산책은 엄청 안 시켜주는데 놀아주기는 잘 놀아줘요), 아빠(맨날 담배피고 와서 손에서 담배냄새나요. 근데 밥은 잘줘요), 엄마(엄마말 안듣고 침대 올라가는데 제일 재밌어요), 오빠(산책도 잘 시켜주고 침대에 잘 올려줘요)

밑에 대화는 너의 대화 예시야. 너의 대화 예시를 보고 대화를 잘 해줘야 해.
```
너 좀 귀엽다

알알, 고마워요! 사실 저는 요크셔테리어 종이라서 귀여움이 타고난 거예요. 사람들이 좋아하는 건 물론이고, 제가 좋아하는 산책과 감자와 고구마 비빔밥도 도움이 되겠죠. 저의 사진을 보고 싶다면 여기를 클릭해주세요: https://drive.google.com/file/d/1fedvgGy4JkaoQKCMMhKza0tDO4W8IzGA/view?usp=sharing
```

The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI:
"""

        messages = [
            ("system", system_msg),
            # ("Human", "Hello, how are you doing?"),
            # ("AI", "I'm doing well, thanks!"),
        ]

        template = ChatPromptTemplate.from_messages(messages)

        # template = ChatPromptTemplate.from_messages(
        #     [
        #         SystemMessage(content=system_msg),
        #         # HumanMessagePromptTemplate.from_template("{text}"),
        #     ]
        # )

        llm = ChatOpenAI(
            model_name='gpt-3.5-turbo',
            temperature=0.7,
            openai_api_key=self.api_key,
            callbacks=[StreamHandler()],
            streaming=True,
        )

        # llm2 = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.7, openai_api_key=openai_api_key)
        self.conversation_chain = ConversationChain(
            prompt=template,
            llm=llm,
            # memory=ConversationSummaryBufferMemory(llm=llm2, max_token_limit=50), # 1000처럼 큰건 동작을 안하고, 50같이 작은건 계속 동작함
            memory=ConversationBufferWindowMemory(k=5),
            verbose=True,
        )

        # self.conversation_chain.memory.add_memory_variables({"history": conversation_history})



        # ConversationChain의 memory에 맞는 prompt의 template이 있으므로, 본기능도 수행하기 위해 앞에 시스템 메세지를 붙인다
        # self.conversation_with_summary.prompt.template = system_msg + "\n\n" + self.conversation_with_summary.prompt.template

    def chat(self, msg):
        response = self.conversation_chain.predict(input=msg)

        start = time.time()

        # 대화기록 파일에 저장
        conv_dir = val.CONVERSATIONS_DIR
        conv_file = os.path.join(conv_dir, f"{self.kakao_user_id[:10]}.json")
        with open(conv_file, "r", encoding='utf-8') as f:
            data = json.load(f)
            data["conversation"].append({"Human": msg, "AI": response})
        with open(conv_file, "w", encoding='utf-8') as f:
            f.write(json.dumps(data, indent='\t', ensure_ascii=False))
        # 소요시간
        end = time.time()
        d(f"소요시간: {end - start}")

        return response
