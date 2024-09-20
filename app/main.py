from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pymongo import MongoClient
from app.handlers.user import UserHandler
from app.handlers.security import APIKeyHandler,JWTHandler
from app.data_services.user import UserService
from app.models.security import Token
from typing import Annotated
import os

# these are secret, need to be taken out in production
secret='Gkq3b7z8J9k8L1k9J8k3L1k9J8k3L1k9J8k3L1k9J8k='
db_uri="mongodb://user:pass@localhost:27017/"
oauth2Scheme=OAuth2PasswordBearer(tokenUrl="token")
# uncoment this line when running in container environment
# db_uri=os.getenv("CONNECTION_STR")
print(db_uri)

# database connection

client=MongoClient(db_uri)
db=client.get_database("testDB")

# initialize data service
user_data_service=UserService(secret,"users",db)

# initialize security handler
apikey_handler=APIKeyHandler(user_data_service)
oauth_handler=JWTHandler(user_data_service,secret,"HS256",5)

app=FastAPI()

# initialize handler
user_handler=UserHandler(user_data_service,apikey_handler,oauth_handler,oauth2Scheme,"User","/users",app)

@app.get("/")
async def root():
    return "Hello people!"

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = user_data_service.login( form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = oauth_handler.create_access_token({"sub": user.email})
    
    return Token(access_token=access_token, token_type="bearer")

@app.get("/test")
async def test_auth(token:Annotated[str,Depends(oauth2Scheme)]):
    result=oauth_handler.verify_token(token)
    if result:
        print("token verified")
    return f"token: {token}"

# register pathes of each handler
user_handler.register_routes()



