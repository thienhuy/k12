import bcrypt

def verify_password(plain_password: str, password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), password.encode())

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
