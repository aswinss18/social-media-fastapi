from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "7bdfdd9b2d07b5eae2b3a33a5e49e1841b7f85e8a7ef4d31c4e8163b2c0dfaa4e3b1eeb2b10b2a99f87c1edb2e5f91aa"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt