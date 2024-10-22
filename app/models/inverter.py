from pydantic import BaseModel
from typing import Annotated
from fastapi import Body

class InverterModel(BaseModel):
    Name: Annotated[str, Body(description="Name of the inverter will be specified for you by the system")]="No Name"
    Vac: Annotated[float, Body(description="Nominal AC voltage (V)")]
    Paco: Annotated[float, Body(description="Maximum AC power (W)")]
    Vdco: Annotated[float, Body(description="Nominal DC voltage (V)")]
    Pso: Annotated[float, Body(description="Power consumption during operation (W)")]
    Vdcmax: Annotated[float, Body(description="Maximum DC voltage (V)")]
    Idcmax: Annotated[float, Body(description="Maximum DC current (A)")]
    Mppt_low: Annotated[float, Body(description="Minimum MPPT DC voltage (V)")]
    Mppt_high: Annotated[float, Body(description="Maximum MPPT DC voltage (V)")]

    diff_Vac: Annotated[float, Body(description="Difference from user-specified Vac")] = 0
    diff_Paco: Annotated[float, Body(description="Difference from user-specified Paco")] = 0
    diff_Vdco: Annotated[float, Body(description="Difference from user-specified Vdco")] = 0
    diff_Pso: Annotated[float, Body(description="Difference from user-specified Pso")] = 0
    diff_Vdcmax: Annotated[float, Body(description="Difference from user-specified Vdcmax")] = 0
    diff_Idcmax: Annotated[float, Body(description="Difference from user-specified Idcmax")] = 0
    diff_Mppt_low: Annotated[float, Body(description="Difference from user-specified Mppt_low")] = 0
    diff_Mppt_high: Annotated[float, Body(description="Difference from user-specified Mppt_high")] = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
