from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from models.building_model import BuildingModel as Building
from util import mongo_db_connector

router = APIRouter(prefix="/buildings", tags=["buildings"])
templates = Jinja2Templates(directory="templates")

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
    buildings_collection = mongo_db_connector.init_buildingsdb("buildings")
    buildings_collection.insert_one(building_data.model_dump())
    return {"message": "Building added successfully", "building": building_data}


@router.put("/{building_id}")
async def update_building(building_data: Building):
    buildings_collection = mongo_db_connector.init_db("buildings")
    buildings_collection.update_one({"id": building_data.id}, {"$set": building_data.model_dump()})
    return {"message": "Building updated successfully", "building": building_data}

@router.get("/{building_id}")
async def read_building(building_id: str):
    """Fetches specific building from the database by building_id."""
    building = await get_buildings(id=building_id)
    return building


async def get_buildings(name: str = None, project: str = None, location: str = None, id: str = None)->list:
    """Fetches sensors from the database depending on received params."""
    buildings_collection = mongo_db_connector.init_buildingsdb("buildings")
    query = {}
    if name:
        query["name"] = name
    if project:
        query["project"] = project
    if location:
        query["location"] = location
    if id:
        query["id"] = id
    buildings = buildings_collection.find(query)
    buildings_return = []
    for building in buildings:
        building.pop("_id")
        buildings_return.append(building)
    return buildings_return
    