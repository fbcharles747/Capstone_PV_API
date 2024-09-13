from fastapi import FastAPI
from pymongo import MongoClient
from app.handlers.user import UserHandler
from app.data_services.user import UserService

# database connection

db_uri="mongodb://user:pass@localhost:27017/"
client=MongoClient(db_uri)
db=client.get_database("testDB")

# initialize data service
user_data_service=UserService("users",db)


app=FastAPI()

# initialize handler
user_handler=UserHandler(user_data_service,"User","/users",app)

@app.get("/")
async def root():
    return "Hello peopl!"

# register pathes of each handler
user_handler.register_routes()



