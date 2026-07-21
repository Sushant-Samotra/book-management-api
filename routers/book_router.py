from fastapi import APIRouter, HTTPException, status
from database import supabase

from models.book_models import (
    BookActionResponse,
    BookCreate,
    BookPatch,
    BookResponse,
    BookUpdate
)

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.get("", response_model=list[BookResponse], status_code=status.HTTP_200_OK)
def get_books():

    try:
        response = (
            supabase.table("books")
            .select("*")
            .execute()
        )
    
    except Exception as error:
        print("GET request error", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable retrive books"
        )

    return response.data

@router.get('/{book_id}',response_model=BookResponse,status_code=status.HTTP_200_OK)
def get_book_by_id(book_id:int):
    try:
        response = (
            supabase.table("books").select("*").eq("id",book_id).execute()
        )
    except Exception as error:
        print('GET/books/book_id error:',error)
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve book"
        )
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return response.data[0]


@router.post("",response_model=BookActionResponse,
             status_code=status.HTTP_201_CREATED)
def create_book(book:BookCreate):
    book_data = book.model_dump()
    try:
        response = (
            supabase.table("books").insert(book_data).select("*").execute()
        )
    except Exception as error:
        print("POST Request Error:",error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Unable to create book")
    if not response.data:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
            detail = "Book was not created")
    return  {
        'message': "Book Created Successfully",
        'book': response.data[0]
    }

@router.put("/{book_id}",response_model=BookActionResponse,status_code=status.HTTP_200_OK)
def put_book(book_id:int,book:BookUpdate):
    update_book = book.model_dump()
    try:
        response = (
            supabase.table("books").update(update_book).eq("id",book_id).select("*").execute()
        )
    except Exception as error:
        print('PUT/books/book_id error:',error)
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to Update book"
        )
    if not response.data:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not Updated"
        )
    return {
        'message': "Book Updated Successfully",
        "book":response.data[0]
    }

@router.patch("/{book_id}",response_model=BookActionResponse,status_code=status.HTTP_200_OK)
def pacth_book(book_id:int,book:BookPatch):
    update_data = book.model_dump(exclude_none=True,exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Any one field is required to update the books")
    try:
        response = (
            supabase.table("books").update(update_data).eq("id",book_id).select("*").execute()
        )
    except Exception as error:
        print('PATCH/books/book_id error:',error)
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to Update data"
        )

    if not response.data:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not Updated"
        )
    return {
        'message': "Book Partial Updated Successfully",
        "book":response.data[0]
    }

@router.delete('/{book_id}',response_model=BookActionResponse,status_code=status.HTTP_200_OK)
def delete_book(book_id:int):
    try:
        response = (
            supabase.table("books").delete().eq("id",book_id).select("*").execute()
        )
    except Exception as error:
        print('DELETE/books/book_id error:',error)
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to Delete Book"
        )
    if not response.data:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not Deleted"
        )
    return {
        'message': "Book Deleted Successfully",
        "book":response.data[0]
    }