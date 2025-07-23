from passlib.context import CryptContext
from datetime import timedelta,datetime
import jwt
from src.config import config
import uuid
import logging

password_context=CryptContext(
    schemes=['bcrypt'],

)
ACCESS_EXPIRY_TIME=3600

def generate_hash_password(password:str):
    hash=password_context.hash(password)
    return hash

def verify_password(password:str,hash_pass:str):
    return password_context.verify(password,hash_pass)

def create_access_token(user_data:dict,expiry_date:timedelta=None,refresh:bool=False):
    payload={}
    payload["user"]=user_data
    exp=datetime.now() + (expiry_date if expiry_date is not None else timedelta(seconds=ACCESS_EXPIRY_TIME))
    payload["exp"]=exp.timestamp()
    payload["jti"]=str(uuid.uuid4())
    payload["refresh"]=refresh

    token=jwt.encode(
        payload=payload,
        key=config.JWT_SECRET,
        algorithm=config.JWT_ALGORITHM

    )
    return token


def decode_token(token:str):
    try:
        token_data=jwt.decode(
            jwt=token,
            key=config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM]

        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

