import os
import sys

import pyyoutube
import requests
from dotenv import load_dotenv
from loguru import logger
from pyyoutube import ChannelListResponse
from requests import ReadTimeout, HTTPError, ConnectionError, RequestException

from configs import CONFIG

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")

logger.configure(**CONFIG)
YT = pyyoutube.Api(api_key=os.environ['API_KEY'])


@logger.catch()
def get_ch_id_by_username(user: str) -> str:
    try:
        resp = requests.get(f"https://yt.lemnoslife.com/channels?handle={user}")
        resp.raise_for_status()
        json_data = resp.json()
        ch_id = json_data.get('items')[0].get('id')
        # assert ch_id != None
    except ConnectionError as e:
        logger.error(f"connection error {e}")
    except ReadTimeout as e:
        logger.error(f"read timeout error {e}")
    except HTTPError as e:
        logger.error(f"http timeout error {e}")
    except RequestException as e:
        logger.error(f"request error {e}")
    except KeyboardInterrupt:
        logger.warning(f"interrupted ...")
    else:
        return ch_id


def get_ch_by_id(channel_id: str) -> ChannelListResponse:
    if channel_id:
        return YT.get_channel_info(channel_id=channel_id)


def get_user_title(ch: ChannelListResponse) -> str:
    if ch:
        title = ch.items[0].snippet.localized.title  # the name of pidar
        return title


def main():
    valid = "user-rs4nu8mv4j"
    # chId = get_ch_id_by_username(valid)
    # ch = get_ch_by_id(chId)
    # title =  get_user_title(ch)
    # lang = detect(title)
    # logger.info(f"{title}:{lang}")


if __name__ == "__main__":
    main()
