from typing import Annotated
from pydantic import BaseModel
from datetime import datetime
from fastapi import Body
class SingleArrayStatus(BaseModel):
  p_mp:Annotated[float,Body(description="dc power output of single array (W)")]
  v_mp:Annotated[float,Body(description="voltage at maximum power (V)")]
  i_mp:Annotated[float,Body(description="current at maximum power (A)")]
  i_sc:Annotated[float,Body(description="short circuit current(A)")]
  v_oc:Annotated[float,Body(description="open circuit voltage (V)")]
  def __init__(self, **kwargs):
        super().__init__(**kwargs)
  
class ModelResult(BaseModel):
  time_stamp:datetime
  calendar_year:Annotated[int,Body(description="year of the time stamp")]
  month:Annotated[int,Body(description="month of the time stamp")]
  day_of_month:Annotated[int,Body(description="days of the month")]
  system_ac_power:Annotated[float,Body(description="ac output power of the system in Watt (W)")]
  system_dc_power:Annotated[float,Body(description='dc output power of all solar panel in Watt (W)')]
  single_array_status:Annotated[SingleArrayStatus,Body(description="modeling result of single array in a system")]
  