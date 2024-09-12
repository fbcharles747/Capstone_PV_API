from app.data_services.base import BaseService
from app.models.user import User

class UserService(BaseService[User]):
    
    def sign_up(self,name:str,password:str):
        user:User=User()
        self.create(user)