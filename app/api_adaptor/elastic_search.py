from elasticsearch import Elasticsearch
from typing import TypeVar,Generic,Union
from pydantic import BaseModel
from app.constant.elastic_search import CalendarInterval


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
    
    def get_fields_matching(self,index:str,lookup:dict)->list[dict]:
        
        matches:list[dict]=[]
        for key,value in lookup:
            matches.append({"match":{key:value}})
        
        resp=self.__client.search(
            index=index,
            size=1000,
            query={
                "bool":{
                    "must":matches
                }
            },
            filter_path="hits.hits,took",
        )

        return resp['hits']['hits']
    
    def get_all(self,index:str):
       resp:dict=self.__client.search(index=index,query={"match_all":{}}) 
       return resp['hits']['hits']
           
    def get_past_24h(self,index:str, timestamp_field:str) -> list[dict]:

        resp:dict=self.__client.search(
            index=index,
            query={
            "range":{
                timestamp_field:{
                    "gte":"now-24h/h",
                    "lte":"now/h"
                }
            }
        },sort=[{timestamp_field:{"order":'asc'}}])
        return resp['hits']['hits']
    
    def get_timebucket_stats(self,index:str,time_stamp_field:str,calendar_interval:CalendarInterval,filters:dict,stats_field:dict):
        matches:list[dict]=[]
        for key,value in filters.items():
            matches.append({"match":{key:value}})

        
        stats_aggs:dict={}

        for key,value in stats_field.items():
            stats_aggs[key]={
                "stats":{
                    "field":value
                }
            }
        
        agg_field:str="analysis"

        resp=self.__client.search(
            index=index,
            query={
                "bool":{
                    "must":matches
                }
            },
            aggs={
                agg_field:{
                    "date_histogram":{
                        "field":time_stamp_field,
                        "calendar_interval":calendar_interval,
                        "min_doc_count": 1
                    },
                    "aggs":stats_aggs
                }
            },
            filter_path="aggregations"
        )
        return resp['aggregations']['analysis']['buckets']


