from fastapi import FastAPI
from app.handlers.user import UserHandler

app=FastAPI()
user_handler=UserHandler(None,"User","/users",app)

@app.get("/")
async def root():
    return "Hello peopl!"

user_handler.register_routes()


