from pydantic import BaseModel
from typing import Optional, List

class SensorModel(BaseModel):
    id: str
    name: str
    address: str
    floors: Optional[int] = 1
    inhabitants: Optional[List[str]] = []
    has_elevator: Optional[bool] = False
    has_parking: Optional[bool] = False