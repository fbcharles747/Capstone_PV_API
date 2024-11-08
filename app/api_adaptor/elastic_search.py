from elasticsearch import Elasticsearch
from typing import TypeVar,Generic
from pydantic import BaseModel


T=TypeVar("T",bound=BaseModel)
class EsAdaptor(Generic[T]):
    def __init__(self, client:Elasticsearch):
        self.__client=client

    def insert(self,index:str,document:T)->bool:
        resp=self.__client.index(
            index=index,
            document=document.model_dump()
        )

        return (resp['result']=='created')or(resp['result']=='updated')

