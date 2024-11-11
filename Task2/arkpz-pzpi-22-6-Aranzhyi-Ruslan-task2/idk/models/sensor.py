from __future__ import annotations

from os import urandom

from tortoise import fields, Model

from idk import models


class Sensor(Model):
    id: int = fields.BigIntField(pk=True)
    owner: models.User = fields.ForeignKeyField("models.User")
    secret_key: str = fields.CharField(max_length=32, default=lambda: urandom(16).hex())
    city: str = fields.CharField(max_length=128)
