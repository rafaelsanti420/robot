import time
import hmac
import hashlib

SECRET = "secret-key"


def create_token(username: str) -> str:
    ts = str(int(time.time()))
    signature = hmac.new(SECRET.encode(), msg=f"{username}:{ts}".encode(), digestmod=hashlib.sha256).hexdigest()
    return f"{username}:{ts}:{signature}"


def verify_token(token: str) -> bool:
    try:
        username, ts, signature = token.split(":")
    except ValueError:
        return False
    expected = hmac.new(SECRET.encode(), msg=f"{username}:{ts}".encode(), digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
