import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from appgoblin_play_scraper.exceptions import ExtraHTTPError, NotFoundError

MAX_RETRIES = 3
RATE_LIMIT_DELAY = 5


def _urlopen(obj, timeout: int | None = None):
    try:
        resp = urlopen(obj, timeout=timeout)
    except HTTPError as e:
        if e.code == 404:
            raise NotFoundError("App not found(404).")
        else:
            raise ExtraHTTPError(
                "App not found. Status code {} returned.".format(e.code)
            )

    return resp.read().decode("UTF-8")


def post(url: str, data: str | bytes, headers: dict) -> str:
    last_exception = None
    rate_exceeded_count = 0
    for _ in range(MAX_RETRIES):
        try:
            resp = _urlopen(Request(url, data=data, headers=headers))
        except Exception as e:
            last_exception = e
            continue
        if "com.google.play.gateway.proto.PlayGatewayError" in resp:
            rate_exceeded_count += 1
            last_exception = Exception("com.google.play.gateway.proto.PlayGatewayError")
            time.sleep(RATE_LIMIT_DELAY * rate_exceeded_count)
            continue
        return resp
    raise last_exception


def get(url: str, timeout: int | None = None) -> str:
    return _urlopen(
        Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            },
        ),
        timeout,
    )
