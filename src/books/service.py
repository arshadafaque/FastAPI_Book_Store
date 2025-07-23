from sqlmodel.ext.asyncio.session import AsyncSession
from .Schemas import BookCreateModel,BookUpdateModel
from sqlmodel import select,desc
from .models import Book
from datetime import datetime,timezone


class BookService:
    async def get_all_book(self,session:AsyncSession):
        statement=select(Book).order_by(desc(Book.created_at))
        result=await session.exec(statement)
        return result.all()

    async def get_book(self,book_id:str,session:AsyncSession):
        statement=select(Book).where(Book.id==book_id)
        result=await session.exec(statement)
        book= result.first()
        return book if book is not None else None

    async def create_book(self,book_data:BookCreateModel,session:AsyncSession):
        book_data_model=book_data.model_dump()
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        book_data_model["created_at"] = now
        book_data_model["updated_at"] = now
        
        new_book=Book(**book_data_model)
        session.add(new_book)
        await session.commit()
        return new_book

    async def update_book(self,book_id:str,book_update:BookUpdateModel,session:AsyncSession):
        book_data=await self.get_book(book_id,session)
        if book_data is not None:
            update_data=book_update.model_dump()
            for k,v in update_data.items():
                setattr(book_data,k,v)
            await session.commit()
            return update_data
        else:
            return None



    async def delete_book(self,book_id:str,session:AsyncSession):
        book_delete= await self.get_book(book_id,session)
        if book_delete is not None:
           await session.delete(book_delete)
           await session.commit()
           return {"message":"Book Delete"}
        else:
           None
