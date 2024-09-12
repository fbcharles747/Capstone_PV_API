from typing import TypeVar,Generic
T= TypeVar("T")
class BaseService(Generic[T]):
    def __init__(self,collection_name:str,db) -> None:
        self.collection=db[collection_name]
    
    def create(self,model:T)->tuple[bool,str]:
        pass

    def read(self,lookup)->T:
        pass

    def update(self,lookup,field_to_change)->tuple[bool,str]:
        pass

    def delete(self,lookup)->tuple[bool,str]:
        pass