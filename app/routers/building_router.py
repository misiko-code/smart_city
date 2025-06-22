from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from models.building_model import BuildingModel as Building
from util import mongo_db_connector
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime,timezone,timedelta


router = APIRouter(prefix="/buildings", tags=["buildings"])
templates = Jinja2Templates(directory="templates")

@router.get("/viewer")
async def building_viewer(request: Request):
    return templates.TemplateResponse("buildingsViewer.html", {"request": request})

@router.get("/management")
async def building_management(request: Request):
    buildings = await get_buildings()
    return templates.TemplateResponse("buildings.html", {"request": request, "buildings": buildings})

@router.get("/")
async def read_buildings():
    """Fetches all buildings from the database."""
    buildings = await get_buildings()
    return buildings

@router.post("/")
async def create_building(building_data: Building):
    building_collection = mongo_db_connector.init_buildingsdb("buildings")
    building_collection.insert_one(building_data.model_dump())
    return {"message": "Building added successfully", "building": building_data}

@router.put("/{building_id}")
async def update_building(building_id: str, building_data: Building):
    buildings_collection = mongo_db_connector.init_buildingsdb("buildings")
    buildings_collection.update_one({"_id": building_id}, {"$set": building_data.model_dump()})
    return {"message": "Building updated successfully", "building": building_data}

@router.get("/{building_id}")
async def read_building(building_id: str):
    """Fetches specific building from the database by building_id."""
    building = await get_buildings(building_id=building_id)
    if not building:
        return {"message": "Building not found"}
    return building

@router.delete("/{building_id}")
async def delete_building(building_id: str):
    buildings_collection = mongo_db_connector.init_buildingsdb("buildings")
    buildings_collection.delete_one({"building_id": building_id})
    return {"message": "Building deleted successfully"}

#--------------------- buildings dict ---------------------
async def get_buildings(building_id: str = None, name: str = None, address: str = None, floor: int = None)->list:
    """Fetches buildings from the database depending on received params."""
    buildings_collection = mongo_db_connector.init_buildingsdb("buildings")
    query = {}
    if building_id:
        query["building_id"] = building_id
    if name:
        query["name"] = name
    if address:
        query["address"] = address
    if floor:
        query["floor"] = floor
    buildings = buildings_collection.find(query)
    buildings_return = []
    for building in buildings:
        building.pop("_id")
        buildings_return.append(building)
    return buildings_return
#--------------------- buildings dict ---------------------
#--------------------- multiuser-editing ---------------------
@router.get("attributes/{building_id}", response_class=HTMLResponse)
async def get_attribute(request: Request, building_id: str):
    db_check_collection = mongo_db_connector.init_buildingsdb("checkversion")
    MAX_LOCK_TIME = timedelta(minutes=10)
    now = datetime.now(timezone.utc)

    # Get the lock document
    lock = db_check_collection.find_one({"name": "checkthelock"})
    
    if not lock:
        # No lock exists, create one and allow editing
        db_check_collection.insert_one({
            "name": "checkthelock",
            "status": 1,
            "timestamp": now
        })
        # Retrieve building data
        result = await get_buildings(building_id = building_id)
        return templates.TemplateResponse("attributes.html", {
            "request": request,
            "buildings": [result] if result else []
        })
    else:        
        lock_status = lock.get("status")
        lock_time = lock.get("timestamp")
        
        # Convert lock_time to timezone-aware if it's not already
        if lock_time and lock_time.tzinfo is None:
            lock_time = lock_time.replace(tzinfo=timezone.utc)

        # If locked and not expired, show warning
        if lock_status == 1 and lock_time and (now - lock_time) < MAX_LOCK_TIME:
            return templates.TemplateResponse("warning.html", {"request": request})

        # Lock expired or not set, allow user to take over
        db_check_collection.find_one_and_update(
            {"name": "checkthelock"},
            {"$set": {"status": 1, "timestamp": now}})
            # Retrieve building data
        result = await get_buildings(building_id = building_id)
        return templates.TemplateResponse("attributes.html", {
            "request": request,
            "buildings": [result] if result else []
        })
    
    # Retrieve building data
    result = await get_buildings(building_id = building_id)
    return templates.TemplateResponse("attributes.html", {
        "request": request,
        "buildings": [result] if result else []
    })
'''
@router.get("attributes/{building_id}")
async def read_attributes(building_id: str, request: Request):
    """Fetches specific building from the database by building_id."""
    building = await get_buildings(building_id=building_id)
    if not building:
        return {"message": "Building not found"}
    return templates.TemplateResponse("attributes.html", {
        "request": request,
        "buildings": [building] if building else []
    })
'''
@router.get("/warning")
async def attribute(request: Request):
    return templates.TemplateResponse("attribute.html", {"request": request})

#--------------------- multiuser-editing ---------------------

