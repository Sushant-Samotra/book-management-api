from fastapi import FastAPI,Depends
from typing import Annotated

app = FastAPI()
def get_message():
    print("This Function is Called")
    return "FastAPI"

@app.get('/home1')
def endpoint(message: Annotated[str,Depends(get_message)]):
    return {
        "message": message,
        "point":"endpoint1"
    }


@app.get('/home2')
def endpoint(message: Annotated[str,Depends(get_message)]):
    return {
        "message": message,
        "point":"endpoint2"
    }

