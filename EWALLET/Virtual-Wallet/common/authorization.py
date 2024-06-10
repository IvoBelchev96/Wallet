from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = 'supersecretkey'
ALGORITHM = 'HS256'
ACCESS_EXPIRE_MINUTES = 60

bearer_scheme = HTTPBearer()

def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: HTTPAuthorizationCredentials, credentials_exception):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception

def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    user_id = verify_access_token(token, credentials_exception)
    return int(user_id)
