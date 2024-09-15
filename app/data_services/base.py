from typing import TypeVar,Generic,Any,Dict,Optional
from pymongo.database import Database

T= TypeVar("T")
class BaseService(Generic[T]):
    def __init__(self,collection_name:str,db:Database):
        self.collection=db.get_collection(name=collection_name)
    
    def create(self,model:T)->bool:
        result=self.collection.insert_one(model.__dict__)
        return result.acknowledged
        

    def read(self,lookup:Dict[str,Any])->Optional[Dict[str,Any]]:
        result=self.collection.find_one(lookup)
        return result

    def update(self,lookup,field_to_change)->tuple[bool,str]:
        pass

    def delete(self,lookup)->tuple[bool,str]:
        pass