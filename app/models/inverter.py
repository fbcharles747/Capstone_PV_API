from pydantic import BaseModel
from typing import Annotated
from fastapi import Body

class InverterModel(BaseModel):
    Name: Annotated[str, Body(description="Name of the inverter")]="No Name"
    Vac: Annotated[float, Body(description="Nominal AC voltage (V)")]
    Paco: Annotated[float, Body(description="Maximum AC power (W)")]
    Pdco: Annotated[float, Body(description="Maximum DC power (W)")]
    Vdco: Annotated[float, Body(description="Nominal DC voltage (V)")]
    Pso: Annotated[float, Body(description="Power consumption during operation (W)")]
    C0: Annotated[float, Body(description="Curvature between AC power and DC power (1/W)")]
    C1: Annotated[float, Body(description="Coefficient of `Pdco` variation with DC input voltage (1/V)")]
    C2: Annotated[float, Body(description="Coefficient of inverter power consumption loss variation with DC input voltage (1/V)")]
    C3: Annotated[float, Body(description="Coefficient of C0 variation with DC input voltage (1/V)")]
    Pnt: Annotated[float, Body(description="Inverter night time loss (kW)")]
    Vdcmax: Annotated[float, Body(description="Maximum DC voltage (V)")]
    Idcmax: Annotated[float, Body(description="Maximum DC current (A)")]
    Mppt_low: Annotated[float, Body(description="Minimum MPPT DC voltage (V)")]
    Mppt_high: Annotated[float, Body(description="Maximum MPPT DC voltage (V)")]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
