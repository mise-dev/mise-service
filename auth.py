from jose import jwt
from pydantic import BaseModel
from decouple import config
from datetime import datetime
from passlib.hash import pbkdf2_sha512

def create_token(user: any) -> str:
    time_diff = 60 * 60 * 24 * 30
    now = datetime.utcnow().timestamp()
    return jwt.encode({
        "name": user.get("name"),
        "uuid": user.get("uuid"),
        "exp": now + time_diff, # expire in 30 days,
        "iat": now,
        "iss": "Mise Service"
    }, key=config("SECRET_KEY"))

def decode_token(token: str) -> any:
    return jwt.decode(token, config("SECRET_KEY"))

def hash_password(password: str) -> str:
    return pbkdf2_sha512.hash(password)
