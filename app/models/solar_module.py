from pydantic import BaseModel
from typing import Annotated
from fastapi import Body

class SolarModuleModel(BaseModel):

    Technology: Annotated[str, Body(description="Technology type of the solar module")]="Mono-c-Si"
    Bifacial: Annotated[int, Body(description="Bifacial indicator (1 for Yes, 0 for No)")] = 1  # New field
    STC: Annotated[float, Body(description="Standard Test Conditions (STC) related values")] = 550.62  # New field
    PTC: Annotated[float, Body(description="Performance Test Conditions (PTC) related values")] = 516.4  # New field
    A_c: Annotated[float, Body(description="Area of singular solar panel (m²)")] = 2.52
    Length: Annotated[float, Body(description="Length of the solar module (m)")] = None  # NaN is represented as None in Python
    Width: Annotated[float, Body(description="Width of the solar module (m)")] = None   # NaN is represented as None in Python
    N_s: Annotated[int, Body(description="Number of cells in series")] = 72
    I_sc_ref: Annotated[float, Body(description="Short circuit current (A) at STC")] = 14
    V_oc_ref: Annotated[float, Body(description="Open circuit voltage (V) at STC")] = 49.9
    I_mp_ref: Annotated[float, Body(description="Max Power Current (A) at STC")] = 13.11
    V_mp_ref: Annotated[float, Body(description="Max power voltage (V) at STC")] = 42
    alpha_sc: Annotated[float, Body(description="Short circuit current change per °C (V/°C)")] = 0.00546
    beta_oc: Annotated[float, Body(description="Open circuit voltage change per °C (V/°C)")] = -0.13024
    T_NOCT: Annotated[float, Body(description="Module NOCT temperature rating (°C)")] = 44.8
    a_ref: Annotated[float, Body(description="Ideality factor (V) from CEC module database")] = 1.82357
    I_L_ref: Annotated[float, Body(description="Reference light current (A)")] = 14.0167
    I_o_ref: Annotated[float, Body(description="Reference diode saturation current (A)")] = 1.78e-11
    R_s: Annotated[float, Body(description="Reference series resistance (Ω)")] = 0.164846
    R_sh_ref: Annotated[float, Body(description="Reference shunt resistance (Ω)")] = 138.077
    Adjust: Annotated[float, Body(description="Temperature coefficient adjustment factor")] = 6.23131
    gamma_r: Annotated[float, Body(description="Gamma (%/°C)")] = -0.33
    BIPV: Annotated[str, Body(description="Bifacial module indicator (Y/N)")] = "N"
    Version: Annotated[str, Body(description="Version of the module")] = "2023.10.31"
    Date: Annotated[str, Body(description="Manufacture date of the module")] = "11/16/2022"
    Name: Annotated[str, Body(description="Name of the solar module")] = "JA Solar JAM72D30-550/MB"  # New field
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
