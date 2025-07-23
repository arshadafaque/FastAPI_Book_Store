from .model import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .Schemas import SignUp
from .utils import generate_hash_password

class UserService:
    async def get_user_by_email(self,email:str,session:AsyncSession):
        statement=select(User).where(User.email==email)
        result =await session.exec(statement)
        users=result.first()
        return users
    async def user_exist(self,email,session:AsyncSession):
        user=await self.get_user_by_email(email,session)
        return True if user is not None else False
    
    async def user_create(self,user_data:SignUp,session:AsyncSession):
        user_data_dict=user_data.model_dump()

        new_user=User(**user_data_dict)
        new_user.password=generate_hash_password(user_data_dict['password'])
        new_user.role="user"
        session.add(new_user)
        await session.commit()
        return new_user
    






        
