import concurrent
import os
import random
import string
import sys
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from langdetect import detect
from loguru import logger
from dotenv import load_dotenv
from configs import CONFIG
from yt import get_ch_id_by_username, get_ch_by_id, get_user_title

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")  # solves RU encoding in output globally

logger.configure(**CONFIG)

LETTERS = string.ascii_lowercase
DIGITS = string.digits
TOTAL_LEN = 10
ATTEMPTS = int(os.environ.get("ATTEMPTS", 100))


def account_generator(num: int = 1000):
    while num:
        base = [random.choice(LETTERS) for _ in range(TOTAL_LEN)]
        base[2] = random.choice(DIGITS)
        base[5] = random.choice(DIGITS)
        base[8] = random.choice(DIGITS)
        ret = ''.join(base)
        yield ret
        num -= 1


def test_orc(token):
    r = requests.get(f"https://www.youtube.com/@{token}")
    return r


def main():
    with ThreadPoolExecutor(max_workers=8) as executor:
        # Start the load operations and mark each future with its URL
        # for p in account_generator(num=10):
        future_to_url = {executor.submit(test_orc, t): t for t in account_generator(num=ATTEMPTS)}
        # future_to_url = {executor.submit(test_orc, t): t for t in ("user-rs4nu8mv4j", "user-rs4nu8mzzz")}
        for future in concurrent.futures.as_completed(future_to_url):
            token = future_to_url[future]
            try:
                response = future.result()
            except Exception as exc:
                logger.error(f"{exc}")
            else:
                if response.status_code == 200:
                    chId = get_ch_id_by_username(token)
                    ch = get_ch_by_id(chId)
                    title = get_user_title(ch)
                    if title:
                        lang = detect(title)
                        if lang == "ru":
                            logger.info(f"OK: https://www.youtube.com/@{token}, {title}")
                # else:
                #     print(f"BAD: https://www.youtube.com/@user-{url}")
    logger.info("DONE")


if __name__ == '__main__':
    main()
