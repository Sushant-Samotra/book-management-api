import os
from datetime import datetime,timezone,timedelta
import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash
from uuid import UUID
from fastapi import HTTPException,status

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES","30"))


if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is required")




# Reusable Instance
password_hash = PasswordHash.recommended()

def hash_password(password : str) -> str:
    return password_hash.hash(password)

def verify_password(original_password: str,hashed_password: str) -> bool:       # hashed_password is  a parameter
    return password_hash.verify(original_password,hashed_password)

def create_access_token(user_id:str) ->str:
    expiration_time = datetime.now(
        timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token_payload = {
        "sub": user_id,
        "exp": expiration_time
    }
    encoded_token = jwt.encode(
        token_payload, JWT_SECRET_KEY,algorithm=JWT_ALGORITHM)
    
    return encoded_token

# def decode_access_token(token:str)->str:
#     try:
#         payload = jwt.decode(
#             token,
#             JWT_SECRET_KEY,
#             algorithm=[JWT_ALGORITHM],
#             options={
#                 "require": ['sub','exp']
#             }
#         )
#     except jwt.ExpiredSignatureError