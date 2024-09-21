from fastapi import FastAPI,Depends,HTTPException,status,Request
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer,APIKeyHeader
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from app.handlers.user import UserHandler
from app.handlers.security import APIKeyHandler,JWTHandler
from app.data_services.user import UserService
from app.models.security import Token
from typing import Annotated
import os

# these are secret, need to be taken out in production
secret='Gkq3b7z8J9k8L1k9J8k3L1k9J8k3L1k9J8k3L1k9J8k='
# db_uri="mongodb://user:pass@localhost:27017/"
oauth2Scheme=OAuth2PasswordBearer(tokenUrl="token")
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
oauth_handler=JWTHandler(user_data_service=user_data_service,
                         secret=secret,
                         algorithm="HS256",
                         expiry_delta=5)

app=FastAPI()

# initialize handler
user_handler=UserHandler(data_service=user_data_service,
                         api_key_handler=apikey_handler,
                         oauth_handler=oauth_handler,
                         tag="User",
                         route="/users",
                         app=app)

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
async def test_auth(authenticated:Annotated[bool,Depends(oauth_handler.verify_token)],
                    apikey_authenticated:Annotated[bool,Depends(apikey_handler.verify_api_key)]):
   
    return f"api key auth: {apikey_authenticated}   oauth auth:{authenticated}"


# register pathes of each handler
user_handler.register_routes()



