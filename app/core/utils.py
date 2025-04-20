from datetime import datetime, timezone, timedelta

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import get_settings
from app.core.models import UserSchema

# Create a PasswordHasher instance
ph = PasswordHasher()


# change 256hex value for every project and make sure to do not change it afterward thank u

# Function to hash a password
def hash_password(psk: str) -> str:
    psk_with_salt = psk + get_settings().salt
    hashed_password = ph.hash(psk_with_salt)
    return hashed_password


# Function to verify user password
def verify_password(hashed_password: str, psk: str) -> bool:
    psk_with_salt = psk + get_settings().salt
    try:
        return ph.verify(hashed_password, psk_with_salt)
    except VerifyMismatchError:
        return False


def create_access_token(user: UserSchema, expires_delta: timedelta = get_settings().access_token_expire_minutes):
    encode = {
        "username": user["username"],
        "id": str(user["id"]),
        "role": user["role"].value,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=expires_delta),
    }
    encode_jwt = jwt.encode(encode, get_settings().secret_key, algorithm=get_settings().algorithm)
    return encode_jwt
