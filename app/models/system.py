from pydantic import BaseModel
from typing import Annotated
from fastapi import Body

from enum import Enum
from typing import Annotated

class MountType(str,Enum):
    FIX = 'fix'
    TRACK = 'track'

class RackingModel(str,Enum):
    GLASS_POLYMER = 'glass_polymer'
    GLASS_GLASS = 'glass_glass'


class FixMount(BaseModel):
    surface_tilt: Annotated[float, Body(description="Surface tilt angle in degrees")] = 45
    surface_azimuth: Annotated[float, Body(description="Surface azimuth angle in degrees")] = 180
    racking_model: Annotated[RackingModel, Body(description="Racking model, either 'glass_polymer' or 'glass_glass'")] = RackingModel.GLASS_POLYMER
    module_height: Annotated[float, Body(description="Module height above ground in meters")] = 1
    def __init__(self,**kwarg):
        super().__init__(**kwarg)

class TrackerMount(BaseModel):
    axis_tilt: Annotated[float, Body(description="Axis tilt angle in degrees")]
    axis_azimuth: Annotated[float, Body(description="Axis azimuth angle in degrees")]
    max_angle: Annotated[float, Body(description="Maximum angle of rotation in degrees")]
    ground_cover_ratio: Annotated[float, Body(description="Ground cover ratio")]
    cross_axis_tilt: Annotated[float, Body(description="Cross-axis tilt angle in degrees")]
    racking_model: Annotated[str, Body(description="Racking model")]
    module_height: Annotated[float, Body(description="Module height above ground in meters")]
    def __init__(self,**kwarg):
        super().__init__(**kwarg)

class SolarArray(BaseModel):
    albedo: Annotated[float, Body(description="Surface albedo")] = 0.25
    modules_per_string: Annotated[int, Body(description="Number of modules per string")] = 25
    strings: Annotated[int, Body(description="Number of strings")] = 1
    mount: Annotated[MountType, Body(description="Mount type, either 'fix' or 'track'")] = MountType.FIX
    fix_mount: Annotated[FixMount, Body(description="Fix mount details, required when mount is 'fix'")] = FixMount()
    track_mount: Annotated[TrackerMount, Body(description="Track mount details, required when mount is 'track'")] = None
    def __init__(self,**kwarg):
        super().__init__(**kwarg)

class PVSystemModel(BaseModel):
    name: Annotated[str, Body(description="Name of the PV system")] = "No name"
    num_of_array: Annotated[int, Body(description="Number of arrays")] = 1
    array_config: Annotated[SolarArray, Body(description="Configuration of the solar array")] = SolarArray()
    def __init__(self,**kwarg):
        super().__init__(**kwarg)
