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

@app.route('/chat', methods=['POST'])
def arong():
    """
    카카오톡 봇에서 보내는 스킬api로 요청이 오면 "안녕"을 보냅니다.
    """
    data = request.get_json()
    d(data)

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
    
    port = 5000
    app.run(debug=True, host='0.0.0.0', port=port, **app_kargs)
    i(f"서버가 {port}포트에서 시작되었습니다")