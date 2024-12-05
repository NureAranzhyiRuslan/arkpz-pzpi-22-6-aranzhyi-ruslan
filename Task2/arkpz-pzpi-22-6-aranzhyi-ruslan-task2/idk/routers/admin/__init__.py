from fastapi import APIRouter

from . import users, cities, sensors, measurements

router = APIRouter(prefix="/admin")

router.include_router(cities.router)
router.include_router(users.router)
router.include_router(sensors.router)
router.include_router(measurements.router)
