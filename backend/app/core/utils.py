from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from app.core.config import get_settings

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



