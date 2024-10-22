from pydantic import BaseModel
from typing import Annotated
from fastapi import Body

class SolarModuleModel(BaseModel):

    Name: Annotated[str, Body(description="Name will be specified by the system")]="Name will be specified by the system"
    I_sc_ref: Annotated[float, Body(description="User-specified Short circuit current (A) at STC")]
    diff_I_sc_ref: Annotated[float, Body(description="Difference from user-specified short circuit current (A)")]=0
    
    V_oc_ref: Annotated[float, Body(description="user-specified Open circuit voltage (V) at STC")]
    diff_V_oc_ref: Annotated[float, Body(description="Difference from user-specified open circuit voltage (V)")]=0
    
    I_mp_ref: Annotated[float, Body(description="User-specified Max Power Current (A) at STC")]
    diff_I_mp_ref: Annotated[float, Body(description="Difference from user-specified max power current (A)")]=0
    
    V_mp_ref: Annotated[float, Body(description="User-specified Max power voltage (V) at STC")]
    diff_V_mp_ref: Annotated[float, Body(description="Difference from user-specified max power voltage (V)")]=0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
