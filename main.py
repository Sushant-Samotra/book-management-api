from fastapi import FastAPI,HTTPException,status
from database import supabase
from routers.book_router import router as book_router

from routers.auth_routes import router as auth_routes

app = FastAPI(
    title = "Supabase Demo",
    description = "Supabase demo with FastAPI"
)

app.include_router(book_router)
app.include_router(auth_routes)

@app.get('/',tags=["Root"])
def home():
    return {
        'message': "Supabase API is running"
    }

# @app.get('/books')
# def get_books():
#     try:
#         response = (
#             supabase.table('books').select('*').execute()
#         )
#         return response.data
#     except Exception as error:
#         print("Database error",error)
#         raise HTTPException(
#             status_code = status.HTTP_503_SERVICE_UNAVAILABLE,
#             deatil = "Unable to retrieve books data from database"
#         )
