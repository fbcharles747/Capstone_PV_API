from typing import TypeVar,Generic,Any,Dict,Optional
from pymongo.database import Database
from bson import ObjectId

T= TypeVar("T")
class BaseService(Generic[T]):
    def __init__(self,collection_name:str,db:Database):
        self.collection=db.get_collection(name=collection_name)
    
    def create(self,model:T)->str|None:
        result=self.collection.insert_one(model.__dict__)
        if result.acknowledged:
            return str(result.inserted_id)
        return None
        

    def read(self,lookup:Dict[str,Any])->Optional[Dict[str,Any]]:
        try:
            result=self.collection.find_one(lookup)
        except Exception as e:
            return None
        return result

    def update(self,lookup:dict,field_to_change:dict)->bool:
        try:
            result=self.collection.update_one(lookup,field_to_change)
            if result.matched_count is 0 or result.modified_count is 0:
                return False
        except Exception:
            return False
        return True

    def delete(self,lookup)->tuple[bool,str]:
        pass