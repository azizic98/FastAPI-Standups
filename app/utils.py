import bcrypt


def hash_password(password: str) -> bytes:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password


def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    return bcrypt.checkpw(password_byte_enc, hashed_password)
