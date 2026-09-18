from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from db import init_db
from repositories import HotelRepository
from services import AvailabilityService


init_db()


app = FastAPI(
    title="Sistema de Reservas Hoteleras",
    description="Prueba técnica AXD",
    version="1.0.0"
)


@app.get("/api")
def api_status():
    return {
        "status": "ok",
        "message": "API de reservas hoteleras funcionando"
    }


@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.get("/api/hotels")
def hotels():
    return HotelRepository.list_hotels()


@app.get("/api/availability")
def availability(
    city: str,
    room_type: str,
    check_in: str,
    check_out: str,
    guests: int = Query(..., ge=1)
):
    try:

        return AvailabilityService.search(
            city,
            room_type,
            check_in,
            check_out,
            guests
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except LookupError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


if os.path.exists("/app/static"):

    app.mount(
        "/assets",
        StaticFiles(directory="/app/static/assets"),
        name="assets"
    )

    @app.get("/{full_path:path}")
    async def frontend(full_path: str):

        return FileResponse(
            "/app/static/index.html"
        )
