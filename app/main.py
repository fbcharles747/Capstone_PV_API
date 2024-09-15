from fastapi import FastAPI
from pymongo import MongoClient
from app.handlers.user import UserHandler
from app.handlers.security import APIKeyHandler
from app.data_services.user import UserService
import os
# these are secret, need to be taken out in production
secret='Gkq3b7z8J9k8L1k9J8k3L1k9J8k3L1k9J8k3L1k9J8k='
# db_uri="mongodb://user:pass@localhost:27017/"

# uncoment this line when running in container environment
db_uri=os.getenv("CONNECTION_STR")
print(db_uri)

# database connection

client=MongoClient(db_uri)
db=client.get_database("testDB")

# initialize data service
user_data_service=UserService(secret,"users",db)

# initialize security handler
apikey_handler=APIKeyHandler(user_data_service)

app=FastAPI()

# initialize handler
user_handler=UserHandler(user_data_service,apikey_handler,"User","/users",app)

@app.get("/")
async def root():
    return "Hello peopl!"

# register pathes of each handler
user_handler.register_routes()



