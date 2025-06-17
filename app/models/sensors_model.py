from pydantic import BaseModel
from typing import Optional, List


class SensorModel(BaseModel):
    sensor_id: str
    location: str
    description: str  # Changed to lowercase
    unit: str
class Sensor_dataModel(BaseModel):
    temperature: float
    humidity: float
   