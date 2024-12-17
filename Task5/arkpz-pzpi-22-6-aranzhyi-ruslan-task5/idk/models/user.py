from __future__ import annotations

from enum import IntEnum

import bcrypt
from tortoise import fields, Model

from idk.utils.enums import Locale, TemperatureUnits


class UserRole(IntEnum):
    USER = 0
    ADMIN = 999


class User(Model):
    id: int = fields.BigIntField(pk=True)
    first_name: str = fields.CharField(max_length=128)
    last_name: str = fields.CharField(max_length=128)
    email: str = fields.CharField(max_length=255)
    password: str = fields.CharField(max_length=255)
    role: UserRole = fields.IntEnumField(UserRole, default=UserRole.USER)
    locale: Locale = fields.IntEnumField(Locale, default=Locale.EN)
    temperature_units: TemperatureUnits = fields.IntEnumField(TemperatureUnits, default=TemperatureUnits.CELSIUS)

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf8"), self.password.encode("utf8"))

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "role": self.role,
            "locale": self.locale,
            "temperature_units": self.temperature_units,
        }
