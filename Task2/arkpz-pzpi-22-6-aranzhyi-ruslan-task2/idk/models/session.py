from __future__ import annotations

from datetime import datetime
from os import urandom

from tortoise import fields, Model

from idk import models, config
from idk.utils.jwt import JWT


class Session(Model):
    id: int = fields.BigIntField(pk=True)
    user: models.User = fields.ForeignKeyField("models.User")
    nonce: str = fields.CharField(max_length=16, default=lambda: urandom(8).hex())
    created_at: datetime = fields.DatetimeField(auto_now_add=True)

    def to_jwt(self) -> str:
        return JWT.encode(
            {
                "u": self.user.id,
                "s": self.id,
                "n": self.nonce,
            },
            config.JWT_KEY,
            expires_in=config.AUTH_JWT_TTL,
        )

    @classmethod
    async def from_jwt(cls, token: str) -> Session | None:
        if (payload := JWT.decode(token, config.JWT_KEY)) is None:
            return

        return await Session.get_or_none(
            id=payload["s"], user__id=payload["u"], nonce=payload["n"]
        ).select_related("user")
