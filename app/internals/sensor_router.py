from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime,timezone
from dateutil import parser

from models.sensors_model import SensorModel as Sensor
from models.sensors_model import Sensor_dataModel as SensorData
from util import mongo_db_connector


internal = APIRouter(prefix="/sensors", tags=["sensors"])
templates = Jinja2Templates(directory="templates")

@internal.get("/management")
async def sensor_management(request: Request):
    sensors = await get_sensors()
    return templates.TemplateResponse("sensors.html", {"request": request, "sensors": sensors})

#--------------------- Sensor Data ---------------------
@internal.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("displaySensor.html", {"request": request})

@internal.post("/sensor_data")
async def receive_sensor_data(data: SensorData, request: Request):
    """Receives sensor data from the frontend and stores it in the database.""" 
    sensorData_collection = mongo_db_connector.init_sensor_datadb("temperature_humidity")
    document = {
        "temperature": data.temperature,
        "humidity": data.humidity,
        "timestamp": datetime.now(timezone.utc).isoformat()  # Use current UTC time
    }
    sensorData_collection.insert_one(document)
    return {"message": "Data received successfully"}

@internal.get("/sensor_data")
async def display_sensor_data():
    sensorData_collection = mongo_db_connector.init_sensor_datadb("temperature_humidity")
    readings= list(sensorData_collection.find().sort("timestamp", -1).limit(100))
    for reading in readings:
        reading["_id"] = str(reading["_id"])  # Convert ObjectId to string
        reading["timestamp"] = parser.parse(reading["timestamp"])  # Convert ISO format to datetime
    return readings
#--------------------- Sensor Data ---------------------

@internal.get("/")
async def read_sensors():
    """Fetches all sensors from the database."""
    sensors = await get_sensors()
    return sensors

@internal.post("/")
async def create_sensor(sensors_data: Sensor):
    sensor_collection = mongo_db_connector.init_sensorsdb("sensors")
    sensor_collection.insert_one(sensors_data.model_dump())
    return {"message": "Sensor added successfully", "sensor": sensors_data}

@internal.get("/{sensor_id}")
async def read_sensors_by_id(sensor_id: str):
    """Fetches specific sensor from the database by sensor_id.."""
    sensors_s = await get_sensors(sensor_id=sensor_id)
    return sensors_s

@internal.put("/{sensor_id}")
async def update_sensor(sensor_id: str, sensor_data: Sensor):
    sensor_collection = mongo_db_connector.init_sensorsdb("sensors")
    sensor_collection.update_one({"sensor_id": sensor_id},{"$set": sensor_data.model_dump()})
    return {"message": "Sensor updated successfully", "sensor": sensor_data}

@internal.delete("/{sensor_id}")
async def delete_sensor(sensor_id: str):
    sensor_collection = mongo_db_connector.init_sensorsdb("sensors")
    sensor_collection.delete_one({"sensor_id": sensor_id})
    return {"message": "Sensor deleted successfully"}


async def get_sensors(sensor_id: str = None, location: str = None,  description: str = None, unit: str = None)->list:
    """Fetches sensors from the database depending on received params."""
    sensors_collection = mongo_db_connector.init_sensorsdb("sensors")
    query = {}
    if sensor_id:
        query["sensor_id"] = sensor_id
    if location:
        query["location"] = location
    if description:
        query["description"] = description  
    if unit:
        query["unit"] = unit
    sensors = sensors_collection.find(query)
    sensors_return = []
    for sensor in sensors:
        sensor.pop("_id")
        sensors_return.append(sensor)
    return sensors_return
    