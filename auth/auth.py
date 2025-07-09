# auth/auth.py
from fastapi import HTTPException
from passlib.context import CryptContext
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError



load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Connect to MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
users_collection = client.journals.users

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def register_user(user_id: str, password: str):
    if users_collection.find_one({"user_id": user_id}):
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed = get_password_hash(password)
    users_collection.insert_one({"user_id": user_id, "hashed_password": hashed})
    return {"msg": "User registered successfully"}


SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(user_id: str, password: str):
    user = users_collection.find_one({"user_id": user_id})
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

#The token is a proof that the user is authenticated.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception