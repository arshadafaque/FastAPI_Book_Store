from fastapi.security import HTTPBearer
from fastapi import Request,status,HTTPException,Depends
from .utils import decode_token
from src.db.redis import token_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from typing import List
from .model import User
user_service=UserService()



class BearerToken(HTTPBearer):
    def __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self,request:Request):
        cred= await super().__call__(request)
        token =cred.credentials
        token_data=decode_token(token)

        if not self.check_token(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expire token"
            )
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"error":"This token is invalid or revoked",
                    "resolution":"get new token" })

        if token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide access token"
            )
        self.verify_access_token(token_data)

        return token_data
    
        
    def check_token(self,token:str):
        valid=decode_token(token)
        return True if valid is not None else False
    
    def verify_access_token(self,token_data:dict):
        raise NotImplementedError("Override into child class")
    

class AccessTokenBearer(BearerToken):
    def verify_access_token(self,token_data:dict):
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide access token"
            )
        
class RefreshTokenBearer(BearerToken):

    def verify_access_token(self,token_data:dict):
        if token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide refresh token"
            )


    

async def get_current_user(
    token_details: dict = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session),
):
    user_email = token_details["user"]["email"]

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not Permitted to access")