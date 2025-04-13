from typing import Annotated, Optional

from msgspec import Struct, Meta


class UserCreate(Struct):
    """Схема создание пользователя"""

    name: str
    surname: str
    password: str


class UserUpdate(Struct):
    """Схема обновление данных пользователя"""

    id: Annotated[int, Meta(ge=1)]
    name: str
    surname: str
    password: Optional[str] = None
