from __future__ import annotations

from tortoise import fields, Model


class City(Model):
    id: int = fields.BigIntField(pk=True)
    name: str = fields.CharField(max_length=128)
    latitude: float = fields.FloatField()
    longitude: float = fields.FloatField()

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }
