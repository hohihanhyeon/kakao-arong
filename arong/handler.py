import threading
import requests
from arong.util import d, i


class Handler(threading.Thread):
    # init
    def __init__(self, pool, request):
        super().__init__()
        self.request = request
        self.pool = pool

    # run() 오버라이딩
    def run(self):
        self.handle()

    def handle(self):
        """
        request는 {}로 callback_url과 data를 키로 가짐
        챗봇에게 응답을 받은 후 callback_url로 응답을 보내는 함수
        """
        callback_url = self.request['callback_url']
        data = self.request['data']
        user_id = data['userRequest']['user']['id']
        user_msg = data['userRequest']['utterance']
        d(f"data, callback_url: {data}, {callback_url}")
        d(f"user_msg: {user_msg}")
        ai_msg = self.pool.get(user_id).chat(user_msg)
        response = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": ai_msg
                        }
                    }
                ]
            }
        }

        # 콜백 url로 POST 응답 보내기
        response = requests.post(callback_url, json=response)

        # 응답 확인
        if response.status_code == 200:
            d("POST 요청이 성공적으로 보내졌습니다.")
        else:
            d(f"POST 요청이 실패했습니다. 응답 코드: {response.status_code}")

        d(f"response: {response.json()}")
