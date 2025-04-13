from typing import Annotated

from litestar import Controller, status_codes, get, post, delete
from litestar.di import Provide
from litestar.params import Parameter
from litestar.exceptions import HTTPException

from . import models, schemas, repository


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
            raise HTTPException(
                detail=f"No user found by id={id}",
                status_code=status_codes.HTTP_404_NOT_FOUND,
            )
        return user

    @post(
        "/update",
        summary="Обновление данных пользователя",
    )
    async def update_one(
        self,
        user_repo: repository.UserRepository,
        data: schemas.UserUpdate,
    ) -> models.User:
        user = await user_repo.get_one_or_none(id=data.id)
        if not user:
            raise HTTPException(
                detail=f"No user found by id={data.id}",
                status_code=status_codes.HTTP_404_NOT_FOUND,
            )

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
        id: int,
    ) -> None:
        await user_repo.delete_where(id=id)
