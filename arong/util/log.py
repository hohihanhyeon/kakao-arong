import logging
# import util
import arong.util as util


def get(name, file="./log.log"):
    """
    이름이 name인 로거를 가져온다.
    
    :param name: 로거 이름
    :param file: 로그 파일 경로 (기본값: ./log.log)
    """

    # file의 부모디렉토리 생성
    util.mkdirs(file)

    # 로거 생성
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        format = "[%(asctime)s] [%(name)s/%(levelname)s] %(message)s"
        formatter = logging.Formatter(fmt=format, datefmt="%H:%M:%S")

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)
        logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(file, mode="w", encoding="utf-8")

        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

    return logger


levels = {
    "d": logging.DEBUG,
    "i": logging.INFO,
    "w": logging.WARNING,
    "e": logging.ERROR,
    "c": logging.CRITICAL,
}


def set_level(name, level):
    """
    로그 레벨을 설정

    :param name: 로거 이름
    :param level: 로그 레벨 (d: debug, i: info, w: warning, e: error, c: critical)
    """

    level = levels[level]
    logger = logging.getLogger(name)
    logger.setLevel(level)
    for handler in logger.handlers:
        handler.setLevel(level)
