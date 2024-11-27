from __future__ import annotations

from os import urandom

from tortoise import fields, Model

from idk import models


class Sensor(Model):
    id: int = fields.BigIntField(pk=True)
    owner: models.User = fields.ForeignKeyField("models.User", null=True)
    secret_key: str = fields.CharField(max_length=32, default=lambda: urandom(16).hex())
    city: models.City = fields.ForeignKeyField("models.City")
    name: str = fields.CharField(max_length=64)

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "secret_key": self.secret_key,
            "city": self.city.to_json(),
            "name": self.name,
        }
