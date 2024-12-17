from __future__ import annotations

from datetime import datetime

from tortoise import fields, Model

from idk import models


class Measurement(Model):
    id: int = fields.BigIntField(pk=True)
    sensor: models.Sensor = fields.ForeignKeyField("models.Sensor")
    temperature: float = fields.FloatField()
    pressure: float = fields.FloatField()
    time: datetime = fields.DatetimeField(auto_now_add=True)

    def to_json(self) -> dict:
        return {
            "temperature": self.temperature,
            "pressure": self.pressure,
            "timestamp": int(self.time.timestamp()),
        }
