"""
- 언어모델 pool을 만들어서 사용해야 할 듯 (또는 언어모델 API 연결딜레이가 적으면 언어모델 생성 후 사용 후 - 삭제해도 괜찮을 듯)
- 사람마다 대화기록을 챗봇이 알고있어야 하므로 단순하게 사용자가 대화를 걸어올 때 챗봇 생성후 대화 전달 (n분마다 검사해서 pool의 마지막대화가 1시간 넘어가면 삭제)
- 사람마다 대화기록이 각각 다르므로 대화기록을 저장해야 함 (대화가 올 때 "data/user-id" 파일에 바로 저장 (user-id: userRequest.user.id의 첫 10자리)
- 챗봇을 만들고 대화를 불러올때는 앞의 k개만 memory전략에 따라서 가공해서 가져오기
- 특정 시간마다 검사해서 마지막대화에서 특정시간이 지났으면 리스트에서 삭제

pool = {
    "user-id": {
        "chatbot": chatbot,
        "last_chat_time": datetime.datetime.now()
    }, ...
}

[프롬프트]
The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
{history}
Human: {input}
AI:

[예시]
The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know.

Current conversation:
Human: 아롱아 안녕 뭐해?
AI: 알알, 안녕하세요! 저는 지금 여기서 여러분과 대화하고 있어요. 어떻게 도와드릴까요?
Human: 강아지가 마우스 먹어도 되?
AI: 알알, 강아지가 마우스를 먹는 것은 좋지 않아요. 마우스는 강아지에게 해로울 수 있는 세균이나 독성 물질을 가질 수 있어요. 또한 마우스를 먹다가 소화기계에 문제가 생길 수도 있어요. 강아지가 마우스를 먹은 경우에는 바로 동물 병원에 연락해서 상담해보시는 것이 좋아요.
Human: 그럼 참외는?
"""
from datetime import datetime
from arong.bot.bot import ArongBot
import val
from arong.util import i


class LLMPool:
    def __init__(self):
        self.pool = {}

    def get(self, bot_id):
        """
        - bot_id에 해당하는 챗봇이 있으면 챗봇을 반환하고, 없으면 새로 생성해서 반환한다.
        """
        if bot_id in self.pool.keys():
            return self.pool[bot_id]["chatbot"]
        else:
            chatbot = ArongBot(val.OPENAI_API_KEY, bot_id)
            self.add(bot_id, chatbot)
            return chatbot

    def update_time(self, bot_id):
        """
        최근시간 업데이트
        """
        self.get(bot_id)["last_chat_time"] = datetime.now()

    def delete(self, bot_id):
        """
        - bot_id에 해당하는 챗봇을 삭제한다.
        """
        del self.pool[bot_id]

    def add(self, bot_id, chatbot):
        """
        - bot_id에 해당하는 챗봇을 추가한다.
        """
        self.pool[bot_id] = {
            "chatbot": chatbot,
            "last_chat_time": datetime.now()
        }

    def check(self):
        """
        일정시간마다 검사해서(스레드 이용) 마지막대화가 1시간 넘어가면 삭제
        """
        now = datetime.now()
        for bot_id in self.pool.keys():
            last_chat_time = self.pool[bot_id]["last_chat_time"]
            if (now - last_chat_time).seconds > val.LAST_CHAT_TIME_LIMIT:
                self.delete(bot_id)
                # 로그 남기기 (삭제된 bot_id와 현재 풀의 개수)
                i(f"삭제된 bot_id: {bot_id}")

        # 현재 풀의 개수 로그 남기기
        i(f"현재 풀: {len(self.pool)}")
