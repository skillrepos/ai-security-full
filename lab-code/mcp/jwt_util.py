"""
Minimal HMAC-signed JWT helper (provided complete).

Dependency-free so the lab runs anywhere. Implements just enough of JWS
(HS256) to issue and verify scoped access tokens. Do NOT use this in
production -- use a vetted library and asymmetric keys.
"""
import base64
import hashlib
import hmac
import json
import time

SECRET = b"omnitech-workshop-demo-secret-change-me"


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def encode(payload: dict, ttl=3600) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    body = dict(payload, iat=int(time.time()), exp=int(time.time()) + ttl)
    seg = f"{_b64(json.dumps(header).encode())}.{_b64(json.dumps(body).encode())}"
    sig = hmac.new(SECRET, seg.encode(), hashlib.sha256).digest()
    return f"{seg}.{_b64(sig)}"


def decode(token: str) -> dict:
    """Return the payload if signature + expiry are valid, else raise."""
    try:
        h, p, s = token.split(".")
    except ValueError:
        raise ValueError("malformed token")
    expected = hmac.new(SECRET, f"{h}.{p}".encode(), hashlib.sha256).digest()
    if not hmac.compare_digest(_unb64(s), expected):
        raise ValueError("bad signature")
    payload = json.loads(_unb64(p))
    if payload.get("exp", 0) < time.time():
        raise ValueError("token expired")
    return payload
