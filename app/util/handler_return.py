from pydantic import BaseModel
from typing import TypeVar,Generic

T=TypeVar("T",bound=BaseModel)

class ResponseWithMsg(BaseModel,Generic[T]):
    message:str
    inserted:bool=False
    result:T

    
class ResponseModifier(Generic[T]):
    def __init__(self):
        super().__init__()
    
    def craft_with_msg(self,msg:str,document:T,inserted:bool=False) -> ResponseWithMsg[T]:

        return ResponseWithMsg[T](
            message=msg,
            inserted=inserted,
            result=document
        )



