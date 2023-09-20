import os
from os.path import join, abspath, dirname, sep

PROJECT_NAME = "arong"
LOG_LEVEL = "d"

# 경로
ROOT_DIR = os.path.dirname(abspath(__file__))
CONVERSATIONS_DIR = join(ROOT_DIR, f"data{sep}conversations")
LOG_DIR = join(ROOT_DIR, "logs")
LATEST_LOG_FILE = join(LOG_DIR, "latest.log")
OPENAI_API_KEY_FILE = join(ROOT_DIR, "openai-api-key.txt")
OPENAI_API_KEY = open(OPENAI_API_KEY_FILE).read()
SERP_API_KEY_FILE = join(ROOT_DIR, "serpapi-api-key.txt")
SERP_API_KEY = open(SERP_API_KEY_FILE).read()

LAST_CHAT_TIME_LIMIT = 60 * 60  # 1시간
