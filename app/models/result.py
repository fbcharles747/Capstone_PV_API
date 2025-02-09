from typing import Annotated
from pydantic import BaseModel
from datetime import datetime,timezone
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
  time_stamp:datetime=datetime.now(tz=timezone.utc)
  calendar_year:Annotated[int,Body(description="year of the time stamp")]=datetime.now(tz=timezone.utc).year
  month:Annotated[int,Body(description="month of the time stamp")]=datetime.now(tz=timezone.utc).month
  day_of_month:Annotated[int,Body(description="days of the month")]=datetime.now(tz=timezone.utc).day
  system_ac_power:Annotated[float,Body(description="ac output power of the system in Watt (W)")]=0
  system_dc_power:Annotated[float,Body(description='dc output power of all solar panel in Watt (W)')]=0
  # single_array_status:Annotated[SingleArrayStatus,Body(description="modeling result of single array in a system")]=None

class StatsResult(BaseModel):
  count:Annotated[int,Body(description="how many data are collected to calculate the min, max, avg and sum")]
  min:Annotated[float,Body(description="the min value among all data point")]
  max:Annotated[float,Body(description="the max value among all data point")]
  avg:Annotated[float,Body(description="the average of all data point")]
  sum:Annotated[float,Body(description="the sum of all data point")]

class AnalyticResult(BaseModel):
  time_stamp:datetime=datetime.now(tz=timezone.utc)
  system_ac_power:Annotated[StatsResult,Body(description="statistic result of system AC power")]
  system_dc_power:Annotated[StatsResult,Body(description='statistic result of system DC power')]
  # single_array_p_mp:Annotated[StatsResult,Body(description='statistic result of single array max power')]
  # single_array_v_mp:Annotated[StatsResult,Body(description='statistic result of single array voltage at max power')]
  # single_array_i_mp:Annotated[StatsResult,Body(description='statistic result of single array current at max power')]
  # single_array_i_sc:Annotated[StatsResult,Body(description='statistic result of single array short circuit current')]
  # single_array_v_oc:Annotated[StatsResult,Body(description='statistic result of single array open circuit voltage')]
