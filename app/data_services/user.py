from pymongo.database import Database
from app.data_services.base import BaseService
from app.models.user import User
from app.models.operation_status import OperationStatus
from fastapi import status
from keycove import hash,encrypt,decrypt,generate_token

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
                  api_key=encrypt(user_api_key,self.__secret_key))
        print("user data generated")
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
    