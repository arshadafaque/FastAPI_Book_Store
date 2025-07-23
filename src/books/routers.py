from fastapi import APIRouter,HTTPException,status,Depends
from src.books.Schemas import Book,BookUpdateModel,BookCreateModel
from typing import List
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer
from src.auth.dependencies import RoleChecker

access_bearer=AccessTokenBearer()    
book_router=APIRouter()
book_servive=BookService()
role_checker=Depends(RoleChecker(["admin","user"]))





@book_router.get("/", response_model=List[Book],dependencies=[role_checker])
async def get_books(session:AsyncSession=Depends(get_session),user_data=Depends(access_bearer)):
    return await book_servive.get_all_book(session)


@book_router.post("/", status_code=status.HTTP_201_CREATED,response_model=Book,dependencies=[role_checker])
async def createbook(book_data:BookCreateModel,session:AsyncSession=Depends(get_session),user_data=Depends(access_bearer)) -> dict:
    new_book = await book_servive.create_book(book_data,session)

    return Book.model_validate(new_book)


@book_router.get("/{book_id}",response_model=Book,dependencies=[role_checker])
async def get_book(book_id: str,session:AsyncSession=Depends(get_session),user_data=Depends(access_bearer)) -> dict:
    get_book= await book_servive.get_book(book_id,session)
    if get_book:
        return get_book
    else:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@book_router.patch("/{book_id}",response_model=BookUpdateModel,dependencies=[role_checker])
async def update_book(book_id: str, book_update_data: BookUpdateModel,session:AsyncSession=Depends(get_session),user_data=Depends(access_bearer)) -> dict:

    update_book= await book_servive.update_book(book_id,book_update_data,session)
    if update_book:
        return update_book
    else:
        raise HTTPException(statuscode=status.HTTP_404_NOT_FOUND, detail="Book not found")


@book_router.delete("/{book_id}",dependencies=[role_checker])
async def delete_book(book_id: str,session:AsyncSession=Depends(get_session),user_data=Depends(access_bearer)):
    delete_book= await book_servive.delete_book(book_id,session)
    if delete_book:
        return {"message":"Book delete"}
    else:
        raise HTTPException(statuscode=status.HTTP_404_NOT_FOUND, detail="Book not found")

