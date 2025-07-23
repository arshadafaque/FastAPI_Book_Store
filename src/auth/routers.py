from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.responses import JSONResponse
from .Schemas import SignUp,SignUpResponse,LoginData
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import create_access_token,decode_token,verify_password
from datetime import timedelta,datetime
from .dependencies import *
from src.db.redis import add_jti_to_blocklist

REFRESH_TOKEN_EXPIRY=2
role_checker=RoleChecker(['admin','user'])


user_service=UserService()

auth_router=APIRouter()

@auth_router.post("/signup",response_model=SignUpResponse,status_code=status.HTTP_201_CREATED)
async def signup(user_data:SignUp,session:AsyncSession=Depends(get_session)):
    email=user_data.email
    exist=await user_service.user_exist(email,session)

    if exist:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User  emails already Exists")
    new_user=await user_service.user_create(user_data,session)
    return new_user


@auth_router.post("/login")
async def login(login_data:LoginData,session:AsyncSession=Depends(get_session)):
    email=login_data.email
    password=login_data.password

    user=await user_service.get_user_by_email(email,session)
    if user is not None:
       pass_valid=verify_password(password,user.password)
       if pass_valid:
           access_token=create_access_token(
               user_data={
                   'email':user.email,
                   'user_id':str(user.id),
                   'role':user.role
               }
           )

           refresh_token=create_access_token(
               user_data={
                   'email':user.email,
                   'user_id':str(user.id),
                   'role':user.role
               },
               refresh=True,
               expiry_date=timedelta(days=REFRESH_TOKEN_EXPIRY)

           )
           return JSONResponse(
               content={
                   "message":"Login SuccessFull",
                   "access_token":access_token,
                   "refresh_token":refresh_token,
                   "users":{
                       "email":user.email,
                       "id":str(user.id)
                   }
               }
           )
       
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Email Password")


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid or expired token")



@auth_router.get("/me")
async def get_current_user(user=Depends(get_current_user),_:bool=Depends(role_checker)):
    return user

@auth_router.get("/logout")
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):

    jti=token_details['jti']
    await add_jti_to_blocklist(jti)

    return JSONResponse(content={"message":"Log out"},
                        status_code=status.HTTP_200_OK)
