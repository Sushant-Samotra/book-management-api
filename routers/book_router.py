from fastapi import APIRouter, HTTPException, status
from database import supabase
from models.book_models import (
    BookCreate,
    BookPatch,
    BookUpdate,
    BookResponse,
    BookActionResponse
)
from dependencies import CurrentAdmin

router = APIRouter(
    prefix='/books',
    tags=["Books"]
)


@router.get(
    "",
    response_model=list[BookResponse],
    status_code=status.HTTP_200_OK
)
def get_books():
    try:
        response = (
            supabase
            .table("books")
            .select("*")
            .execute()
        )
    except Exception as error:
        print("GET request error:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable retrieve books"
        )
    return response.data


@router.get(
    '/{book_id}',
    response_model=BookResponse,
    status_code=status.HTTP_200_OK
)
def get_book_by_id(book_id: int):
    try:
        response = (
            supabase
            .table("books")
            .select("*")
            .eq("id", book_id)
            .execute()
        )
    except Exception as error:
        print("GET /books/book_id error:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retreive book"
        )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return response.data[0]


@router.post(
    '',
    response_model=BookActionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(book: BookCreate, current_user: CurrentAdmin):
    book_data = book.model_dump()
    try:
        response = (
            supabase
            .table("books")
            .insert(book_data)
            .select("*")
            .execute()
        )
    except Exception as error:
        print("POST Request error:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create book"
        )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Book was not created"
        )
    return {
        "message": "Book created successfully",
        "book": response.data[0]
    }


@router.put(
    "/{book_id}",
    response_model=BookActionResponse,
    status_code=status.HTTP_200_OK
)
def update_book(book_id: int, book: BookUpdate, current_user: CurrentAdmin):
    update_book = book.model_dump()
    try:
        response = (
            supabase
            .table("books")
            .update(update_book)
            .eq("id", book_id)
            .select("*")
            .execute()
        )
    except Exception as error:
        print("PUT Request error:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="unable to update book"
        )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return {
        "message": "Book updated successfully",
        "book": response.data[0]
    }


@router.patch(
    "/{book_id}",
    response_model=BookActionResponse,
    status_code=status.HTTP_200_OK
)
def patch_book(book_id: int, book: BookPatch, current_user: CurrentAdmin):
    patch_book = book.model_dump(
        exclude_unset=True,
        exclude_none=True
    )
    if not patch_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Any one field is required to update the books"
        )
    try:
        response = (
            supabase
            .table("books")
            .update(update_book)
            .eq("id", book_id)
            .select("*")
            .execute()
        )
    except Exception as error:
        print("PATCH Request error:", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="unable to update book"
        )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return {
        "message": "Book partial update successfully",
        "book": response.data[0]
    }


@router.delete(
    "/{book_id}",
    response_model=BookActionResponse,
    status_code=status.HTTP_200_OK
)
def delete_book(book_id: int, current_user: CurrentAdmin):
    try:
        response = (
            supabase
            .table("books")
            .delete()
            .eq("id", book_id)
            .select("*")
            .execute()
        )
    except Exception as error:
        print("Delete Request error", error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to Delete Books"
        )
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not Found"
        )
    return {
        "message": "Book Deleted Successfully",
        "book": response.data[0]
    }