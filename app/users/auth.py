import hashlib
from datetime import datetime, timedelta
import jwt

from app.config import ACCESS_SECRET_KEY, ALGORITHM



def get_password_hash(email: str, password: str) -> str:
    return hashlib.sha256((email + password).encode('utf-8')).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashlib.sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=2000)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, ACCESS_SECRET_KEY, ALGORITHM)
    return encode_jwt

