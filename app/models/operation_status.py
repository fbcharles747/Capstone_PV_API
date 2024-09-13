from pydantic import BaseModel
class OperationStatus(BaseModel):
    status_code:int
    acknowledged:bool
    message:str

