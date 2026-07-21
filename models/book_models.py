from typing import Optional

from pydantic import BaseModel


# Request body for creating a new book.
class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    language: str


# Request body for replacing all editable fields.
class BookUpdate(BaseModel):
    title: str
    author: str
    genre: str
    language: str


# Request body for updating selected fields.
class BookPatch(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    language: Optional[str] = None


# Public response shape for one book.
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    language: str


# Response shape for create, update, patch, and delete.
class BookActionResponse(BaseModel):
    message: str
    book: BookResponse