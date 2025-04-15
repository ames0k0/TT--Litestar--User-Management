from typing import Optional

from msgspec import Struct


class UserCreate(Struct):
    """Схема создание пользователя"""

    name: str
    surname: str
    password: str


class UserUpdate(Struct):
    """Схема обновление данных пользователя"""

    name: str
    surname: str
    password: Optional[str] = None
