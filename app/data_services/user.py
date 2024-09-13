from app.data_services.base import BaseService
from app.models.user import User

class UserService(BaseService[User]):
    
    def sign_up(self,email:str,password:str):
        user=User(email=email,password=password)
        self.create(user)