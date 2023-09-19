import sys

from flask import Flask, request, send_file, jsonify

import arong.util as util
import val
from arong.bot.pool import LLMPool
from arong.handler import Handler
from arong.util import i, d

app = Flask(__name__)


@app.route('/')
def index():
    return send_file('./web/index.html')


def setup_ssl():
    from flask_sslify import SSLify  # SSL 적용을 위한 모듈

    ssl_home = '/etc/letsencrypt/live/arong.r-e.kr/'
    ssl_fullchain = ssl_home + 'fullchain.pem'
    ssl_privkey = ssl_home + 'privkey.pem'

    # SSL 적용
    return SSLify(app), ssl_fullchain, ssl_privkey


def configs():
    pass


@app.route('/test', methods=['POST'])
def test_response():
    """
    카카오톡 봇에서 보내는 스킬api로 요청이 오면 "안녕"을 보냅니다.
    """
    data = request.get_json()
    d(f"/test: {data}")

    response = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕"
                    }
                }
            ]
        }
    }
    return jsonify(response), 200


@app.route('/chat', methods=['POST'])
def chat_response():
    """
    카카오톡 봇에서 보내는 스킬api로 요청이 언어모델이 적절한 답변을 보냅니다.
    """
    data = request.get_json()
    d(f"/bot: {data}\n\n")

    # callBackUrl 추출하기
    callback_url = data['userRequest']['callbackUrl']
    d(f"callback_url: {callback_url}")

    # response_callback()함수를 비동기적로 실행한 다음에 바로 200 응답을 보내기
    # response_callback(data, callback_url)
    # global _data, _callback_url
    # _data, _callback_url = data, callback_url
    # threading.Thread(target=respond_callback).start()

    handler_data = {
        "callback_url": callback_url,
        "data": data
    }
    handler = Handler(pool, handler_data)
    handler.start()

    response = {
        "version": "2.0",
        "useCallback": True,
        "data": {
            "text": "알알"
        }
    }
    return jsonify(response), 200


# def respond_callback():
#     d(f"_data, _callback_url: {_data}, {_callback_url}")
#     # 사용자의 메세지 추출하기
#     user_msg = _data['userRequest']['utterance']
#     d(f"user_msg: {user_msg}")
#
#     ai_msg = arong.chat(user_msg)
#
#     response = {
#         "version": "2.0",
#         "template": {
#             "outputs": [
#                 {
#                     "simpleText": {
#                         "text": ai_msg
#                     }
#                 }
#             ]
#         }
#     }
#
#     # 콜백 url로 POST 응답 보내기
#     response = requests.post(_callback_url, json=response)
#
#     # 응답 확인
#     if response.status_code == 200:
#         d("POST 요청이 성공적으로 보내졌습니다.")
#     else:
#         d(f"POST 요청이 실패했습니다. 응답 코드: {response.status_code}")
#
#     d(f"response: {response.json()}")

def setup():
    # data/conversations 폴더 생성
    util.mkdirs(val.CONVERSATIONS_DIR)
    # logs 폴더 생성
    util.mkdirs(val.LOG_DIR)


if __name__ == '__main__':
    # app configs 설정
    configs()
    pool = LLMPool()

    # 인자 가져와서 ssl 실행 유뮤 결정
    argv = sys.argv[1:]
    # python app.py --ssl
    app_kargs = {}
    if '--ssl' in argv:
        i("ssl 적용됨")
        _, ssl_fullchain, ssl_privkey = setup_ssl()
        app_kargs['ssl_context'] = (ssl_fullchain, ssl_privkey)

    port = 11418
    app.run(debug=True, host='0.0.0.0', port=port, **app_kargs)
    i(f"서버가 {port}포트에서 시작되었습니다")

    # 서버 시작 후 코드는 서버 끝난 후 실행됨
