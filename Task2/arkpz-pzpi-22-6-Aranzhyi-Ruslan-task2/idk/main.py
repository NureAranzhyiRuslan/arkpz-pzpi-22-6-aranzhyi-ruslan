from fastapi import FastAPI

from .routers import auth, user, sensors, measurements, forecast

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(sensors.router)
app.include_router(measurements.router)
app.include_router(forecast.router)
