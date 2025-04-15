from typing import Annotated

from litestar import Controller, get, post, delete
from litestar.di import Provide
from litestar.params import Parameter

from src.core import exceptions
from . import models, schemas, repository


# TODO: provide `user` for a given `id`


class UsersController(Controller):
    """Контроллер для управления пользователями"""

    path = "/users"
    tags = ["users"]
    dependencies = {
        "user_repo": Provide(repository.provide_user_repo),
    }
    return_dto = models.UserReadDTO

    @post(
        "/create",
        summary="Создание пользователя",
    )
    async def create_one(
        self,
        user_repo: repository.UserRepository,
        data: schemas.UserCreate,
    ) -> models.User:
        return await user_repo.add(
            models.User(
                name=data.name,
                surname=data.surname,
                password=data.password,
            )
        )

    @get(
        "/get_all",
        summary="Получение списка пользователей",
    )
    async def get_all(
        self,
        user_repo: repository.UserRepository,
    ) -> list[models.User]:
        return await user_repo.list()

    @get(
        "/get",
        summary="Получение данных одного пользователя",
    )
    async def get_one(
        self,
        user_repo: repository.UserRepository,
        id: Annotated[
            int,
            Parameter(ge=1, description="Идентификатор пользователя"),
        ],
    ) -> models.User:
        user = await user_repo.get_one_or_none(id=id)
        if not user:
            raise exceptions.UserNotFound(user_id=id)
        return user

    @post(
        "/update",
        summary="Обновление данных пользователя",
    )
    async def update_one(
        self,
        user_repo: repository.UserRepository,
        id: Annotated[
            int,
            Parameter(ge=1, description="Идентификатор пользователя"),
        ],
        data: schemas.UserUpdate,
    ) -> models.User:
        user = await user_repo.get_one_or_none(id=id)
        if not user:
            raise exceptions.UserNotFound(user_id=id)

        user.name = data.name
        user.surname = data.surname

        if data.password:
            user.password = data.password

        return await user_repo.update(user)

    @delete(
        "/delete",
        return_dto=None,
        summary="Удаление пользователя",
    )
    async def delete_one(
        self,
        user_repo: repository.UserRepository,
        id: Annotated[
            int,
            Parameter(ge=1, description="Идентификатор пользователя"),
        ],
    ) -> None:
        await user_repo.delete_where(id=id)
