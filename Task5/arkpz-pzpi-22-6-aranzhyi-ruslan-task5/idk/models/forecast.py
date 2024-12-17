from __future__ import annotations

from datetime import datetime

from tortoise import fields, Model

from idk import models


class Forecast(Model):
    id: int = fields.BigIntField(pk=True)
    city: models.City = fields.ForeignKeyField("models.City")
    info_text: str = fields.CharField(max_length=128)
    temperature: float = fields.FloatField()
    timestamp: datetime = fields.DatetimeField(auto_now_add=True)

    def to_json(self) -> dict:
        return {
            "info_text": self.info_text,
            "temperature": self.temperature,
            "details": {
                "has_details": False,
            }
        }
