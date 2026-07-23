import time
from fastapi import FastAPI,HTTPException,status,Request
from database import supabase
from routers.book_router import router as book_router

from routers.auth_routes import router as auth_routes

app = FastAPI(
    title = "Supabase Demo",
    description = "Supabase demo with FastAPI"
)

app.include_router(book_router)
app.include_router(auth_routes)

@app.middleware("http")
async def request_metrics(request:Request,call_next):
    # Time starts once request is received
    start_time = time.perf_counter()

    # We are calling api and writing untill its response
    response = await call_next(request)

    # Check process time by getting current-time and check defference with start time
    process_time = time.perf_counter() - start_time

    # adding process time to header response
    response.headers["X-Process_Time"] = f"{process_time:.4f}"

    print(request.method, request.url.path,response.status_code,f"{process_time:.4f}")

    return response

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
