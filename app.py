from arong import chat
import sys
import json
from flask import Flask, request, send_file, jsonify
import os
import arong.util as util
import arong.util.log as log

app = Flask(__name__)

@app.route('/')
def index():
    return send_file('./web/index.html')

def setup_ssl():
    from flask_sslify import SSLify  # SSL 적용을 위한 모듈

    ssl_home = '/etc/letsencrypt/live/arong.r-e.kr/'
    global ssl_fullchain 
    ssl_fullchain = ssl_home + 'fullchain.pem'
    global ssl_privkey 
    ssl_privkey = ssl_home + 'privkey.pem'

    # SSL 적용
    return SSLify(app)

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
    d(f"/chat: {data}")

    # 사용자의 메세지 추출하기
    user_msg = data['userRequest']['utterance']
    d(f"user_msg: {user_msg}")

    ai_msg = chat(user_msg)

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
    return jsonify(response), 200


if __name__ == '__main__':
    # app configs 설정
    configs()

    # 로거
    logger = log.get(__name__, f"./logs/{__name__}.log")
    log.set_level(__name__, "d")
    i, d = logger.info, logger.debug

    # 인자 가져와서 ssl 실행 유뮤 결정
    argv = sys.argv[1:]
    # python app.py --ssl
    app_kargs = {}
    if '--ssl' in argv:
        i("ssl 적용됨")
        setup_ssl()
        app_kargs['ssl_context'] = (ssl_fullchain, ssl_privkey)
    
    port = 11418
    app.run(debug=True, host='0.0.0.0', port=port, **app_kargs)
    i(f"서버가 {port}포트에서 시작되었습니다")
