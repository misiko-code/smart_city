from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from models.building_model import BuildingModel as Building
from util import mongo_db_connector


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
