from datetime import datetime
import val
from arong.util import log
import json
import os


def mkdirs(file):
    parent_dir = os.path.dirname(file)
    os.makedirs(parent_dir, exist_ok=True)


def pprint(d):
    """
    Pretty print
    """
    print(pprints(d))


def pprints(d):
    """
    Pretty print string
    """
    return json.dumps(d, indent="\t")


# 로거
def _setup_log():
    global logger_inited
    if logger_inited is True:
        return logger

    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%dT%H;%M;%S")
    _logger = log.get(val.PROJECT_NAME, os.path.join(val.LOG_DIR, f"{formatted_datetime}.log"))
    log.set_level(val.PROJECT_NAME, val.LOG_LEVEL)
    logger_inited = True
    return _logger


logger_inited = False
logger = _setup_log()
i, d = logger.info, logger.debug
