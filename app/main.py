from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from routers.building_router import router as building_router
from internals.sensor_router import internal as sensor_internal

app = FastAPI()

app.include_router(building_router)
app.include_router(sensor_internal)
app.mount("/static", StaticFiles(directory="static"), name = "static")

@app.get("/")
def read_root():
        return RedirectResponse("/buildings/viewer", status_code=303)

