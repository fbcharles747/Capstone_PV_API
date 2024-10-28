from pydantic import BaseModel
from typing import Annotated
from fastapi import Body

class SolarModuleModel(BaseModel):

    Technology: Annotated[str, Body(description="Technology type of the solar module")]='not required'
    Bifacial: Annotated[int, Body(description="Bifacial indicator (1 for Yes, 0 for No)")]
    STC: Annotated[float, Body(description="Standard Test Conditions (STC) related values")]
    PTC: Annotated[float, Body(description="Performance Test Conditions (PTC) related values")]
    A_c: Annotated[float, Body(description="Area of singular solar panel (m²)")]
    Length: Annotated[float, Body(description="Length of the solar module (m)")]
    Width: Annotated[float, Body(description="Width of the solar module (m)")]
    N_s: Annotated[int, Body(description="Number of cells in series")]
    I_sc_ref: Annotated[float, Body(description="Short circuit current (A) at STC")]
    V_oc_ref: Annotated[float, Body(description="Open circuit voltage (V) at STC")]
    I_mp_ref: Annotated[float, Body(description="Max Power Current (A) at STC")]
    V_mp_ref: Annotated[float, Body(description="Max power voltage (V) at STC")]
    alpha_sc: Annotated[float, Body(description="Short circuit current change per °C (V/°C)")]
    beta_oc: Annotated[float, Body(description="Open circuit voltage change per °C (V/°C)")]
    T_NOCT: Annotated[float, Body(description="Module NOCT temperature rating (°C)")]
    a_ref: Annotated[float, Body(description="Ideality factor (V) from CEC module database")]
    I_L_ref: Annotated[float, Body(description="Reference light current (A)")]
    I_o_ref: Annotated[float, Body(description="Reference diode saturation current (A)")]
    R_s: Annotated[float, Body(description="Reference series resistance (Ω)")]
    R_sh_ref: Annotated[float, Body(description="Reference shunt resistance (Ω)")]
    Adjust: Annotated[float, Body(description="Temperature coefficient adjustment factor")]
    gamma_r: Annotated[float, Body(description="Gamma (%/°C)")]
    BIPV: Annotated[str, Body(description="Bifacial module indicator (Y/N)")]
    Version: Annotated[str, Body(description="Version of the module")]='not required'
    Date: Annotated[str, Body(description="Manufacture date of the module")]='not required'
    Name: Annotated[str, Body(description="Name of the solar module")]='not required'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
