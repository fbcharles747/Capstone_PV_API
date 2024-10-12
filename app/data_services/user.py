from pymongo.database import Database
from app.data_services.base import BaseService
from app.models.user import User
from app.models.operation_status import OperationStatus
from app.models.security import Token
from fastapi import status
from keycove import hash,encrypt,decrypt,generate_token
from typing import Optional

class UserService(BaseService[User]):

    def __init__(self,secret_key:str ,collection_name: str, db: Database):
        super().__init__(collection_name, db)
        self.__secret_key=secret_key
    
    def sign_up(self,email:str,password:str)->OperationStatus:
        if self.read({"email":email})!=None:
            return OperationStatus(acknowledged=False,
                                   status_code=status.HTTP_409_CONFLICT,
                                   message="user already exists")
        
        user_api_key=generate_token()
        user=User(email=email,
                  password=hash(password),
                  hashed_api_key=hash(user_api_key),
                  encrypt_api_key=encrypt(user_api_key,self.__secret_key)
                  )
        if self.create(user):
            return OperationStatus(
                status_code=status.HTTP_201_CREATED,
                acknowledged=True,
                message="user created"
            )
        else:
            return OperationStatus(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                acknowledged=False,
                message="server error"
            )
    
    def get_by_email(self,email:str)->Optional[User]:
        result=self.read({"email":email})
        if result is not None:
            return User(**result)
        return None
    
    def get_by_apikey(self,api_key:str)->Optional[User]:
        hashed_apikey=hash(api_key)
        result=self.read({"hashed_api_key":hashed_apikey})

        if result is not None:
            return User(**result)
        return None
    
    def decrypt_apikey(self, encypt_str:str)->str:
        return decrypt(encrypted_value=encypt_str,secret_key=self.__secret_key)
    
    def login(self,email:str,password:str)-> Optional[User]:
        result=self.read({"email":email,"password":hash(password)})
        if result is not None:
            return User(**result)
        return None
    
    def update_by_email(self,email:str,update_dict:dict):
        return self.update(
            {"email":email},
            update_dict
        )
    
    def update_locationId(self,user_email:str,locationId:str)->bool:
        return self.update_by_email(user_email,{'location_Id':locationId})
    
    def update_inverterId(self,user_email:str,inverterId:str|None)->bool:
        return self.update_by_email(user_email,{'inverter_Id':inverterId})
    
    def update_moduleId(self,user_email:str,moduleId:str|None)->bool:
        return self.update_by_email(user_email,{'solarModule_Id':moduleId})
    
    def toggle_apikey(self, email:str,enable:bool)->bool:
        return self.update_by_email(email=email,update_dict={"api_key_enable":enable})

    
