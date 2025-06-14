from pydantic import BaseModel
from typing import Optional, List
import datetime

class SensorModel(BaseModel):
    sensor_id: str
    Description: str
    location: str
    unit: str
    enabled: Optional[bool] = False
    type: Optional[bool] = False
    value: Optional[bool] = False

class Sensor_dataModel(BaseModel):
    temperature:float
    humidity:float
    timestamp: datetime.datetime