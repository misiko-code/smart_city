from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from models.sensors_model import SensorModel as Sensor
from util import mongo_db_connector

internal = APIRouter(prefix="/sensors", tags=["sensors"])
templates = Jinja2Templates(directory="templates")

@internal.get("/management")
async def sensor_management(request: Request):
    sensors = await get_sensors()
    return templates.TemplateResponse("sensors.html", {"request": request, "sensors": sensors})


@internal.get("/")
async def read_sensors():
    """Fetches all sensors from the database."""
    sensors = await get_sensors()
    return sensors

@internal.post("/")
async def create_sensor(sensor_data: Sensor):
    sensor_collection = mongo_db_connector.int_sensorsdb("sensors")
    sensor_collection.insert_one(sensor_data.model_dump())
    return {"message": "Sensor added successfully", "sensor": sensor_data}

@internal.get("/{sensor_id}")
async def read_sensors(sensor_id: str):
    """Fetches specific sensor from the database by sensor_id.."""
    sensors_s = await get_sensors(id= sensor_id)
    return sensors_s

@internal.put("/{sensor_id}")
async def update_sensor(sensor_data: Sensor):
    sensor_collection = mongo_db_connector.init_sensorsdb("sensors")
    sensor_collection.update_one({"id": sensor_data.id},{"$set": sensor_data.model_dump()})
    return {"message": "Sensor updated successfully", "sensor": sensor_data}

@internal.delete("/{sensor_id}")
async def delete_sensor(sensor_data: Sensor):
    sensor_collection = mongo_db_connector.init_sensorsdb("sensors")
    sensor_collection.delete_one({"id": sensor_data.id})
    return{"message": "Item deleted successfully"}


async def get_sensors(name: str = None, project: str = None, location: str = None, id: str = None)->list:
    """Fetches buildings from the database depending on received params."""
    sensors_collection = mongo_db_connector.init_sensorsdb("sensors")
    query = {}
    if name:
        query["name"] = name
    if project:
        query["project"] = project
    if location:
        query["location"] = location
    if id:
        query["id"] = id
    sensors = sensors_collection.find(query)
    sensors_return = []
    for sensor in sensors:
        sensor.pop("_id")
        sensors_return.append(sensor)
    return sensors_return
    