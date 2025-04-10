import datetime

import msgspec


class UserCreatePayload(msgspec.Struct):
    name: str
    surname: str
    password: str


class UserInDB(UserCreatePayload):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserUpdatePayload(msgspec.Struct):
    name: str | None
    surname: str | None
    password: str | None
