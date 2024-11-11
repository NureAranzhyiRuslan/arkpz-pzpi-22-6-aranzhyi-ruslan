from __future__ import annotations

from enum import IntEnum

from tortoise import fields, Model


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
