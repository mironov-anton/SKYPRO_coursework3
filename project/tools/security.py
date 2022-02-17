import base64
import hashlib
import hmac
from typing import Union

from flask import current_app


def get_password_digest(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config['PWD_HASH_SALT'],
        iterations=current_app.config['PWD_HASH_ITERATIONS']
    )


def get_password_hash(password) -> str:
    return base64.b64encode(get_password_digest(password)).decode("utf-8")


def compare_passwords(hash_password: Union[str, bytes], password: str) -> bool:
    return hmac.compare_digest(
        base64.b64decode(hash_password),
        get_password_digest(password)
    )
