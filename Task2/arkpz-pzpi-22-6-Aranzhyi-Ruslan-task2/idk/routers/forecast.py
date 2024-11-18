from datetime import timedelta, datetime

from fastapi import APIRouter
from pytz import UTC

from idk.dependencies import SensorDep
from idk.models import Measurement
from idk.schemas.forecast import ForecastResponse

AVERAGE_ALTITUDE = 150  # Meters (Ukraine)
WINTER_MONTHS = (12, 1, 2)
SUMMER_MONTHS = (6, 7, 8)

router = APIRouter(prefix="/forecast")


def calculate_zambretti_method(measurements: list[dict[str, str | float]], real_count: int | None = None) -> dict:
    pressure_mts = [measurement["pressure"] for measurement in measurements]

    # Pressure trend
    count = len(pressure_mts)
    sum_x = count / 2 * (count - 1)
    sum_y = sum(pressure_mts)
    sum_x_sq = count * (count + 1) * (2 * count + 1) / 6
    sum_xy = sum(map(lambda item: item[0] * item[1], enumerate(pressure_mts)))
    a = count * sum_xy - sum_x * sum_y
    a /= count * sum_x_sq - sum_x * sum_x
    pressure_delta = a * count

    altitude = 0.0065 * AVERAGE_ALTITUDE
    p0 = pressure_mts[-1] * ((1 - altitude / (measurements[-1]["temperature"] + altitude + 273.15)) ** (-5.257))
    if pressure_delta >= 1:
        z = 179 - 2 * p0 / 128
    elif pressure_delta <= -1:
        z = 130 - p0 / 81
    else:
        z = 147 - 5 * p0 / 376

    this_month = datetime.now().month
    if this_month in WINTER_MONTHS and pressure_delta <= -1:
        z -= 1
    elif this_month in SUMMER_MONTHS and pressure_delta >= 1:
        z += 1

    z = int(z)

    return {
        "info_text": "TODO",
        "temperature": 0,  # TODO: calculate temperature
        "details": {
            "measurements_count": count,
            "measurements_db_count": real_count or count,
            "pressure_average": sum_y / count,
            "pressure_delta": pressure_delta,
            "p0": p0,
            "z": z,
        }
    }


@router.post("/{sensor_id}", response_model=ForecastResponse)
async def get_sensor_forecast_zambretti(sensor: SensorDep):
    measurements = await Measurement.filter(
        sensor=sensor, time_gt=(datetime.now(UTC) - timedelta(days=1))
    ).order_by("time")

    return calculate_zambretti_method([
        {
            "pressure": measurement.pressure,
            "temperature": measurement.temperature,
        }
        for measurement in measurements
    ])


@router.get("/city", response_model=ForecastResponse)
async def get_city_forecast(city: int | str):
    query = {
        "time__gt": datetime.now(UTC) - timedelta(days=1),
        "sensor__city__name" if isinstance(city, str) else "sensor__city__id": city
    }
    measurements_all = await Measurement.filter(*query).order_by("time")
    measurements = []
    for measurement in measurements_all:
        time_section = int(measurement.time.timestamp()) % (60 * 30)
        if not measurements or measurements[-1]["time"] != time_section:
            if measurements:
                pressure_items = measurements[-1]["pressure_items"]
                temp_items = measurements[-1]["temperature_items"]
                measurements[-1]["pressure"] = len(sum(*pressure_items) / len(pressure_items))
                measurements[-1]["temperature"] = len(sum(*temp_items) / len(temp_items))
                del measurements[-1]["pressure_items"]
                del measurements[-1]["temp_items"]

            measurements.append({
                "time": time_section,
                "pressure_items": [],
                "temperature_items": [],
            })

        measurements[-1]["pressure_items"].append(measurement.pressure)
        measurements[-1]["temperature_items"].append(measurement.temperature)

    return calculate_zambretti_method(measurements, len(measurements_all))
