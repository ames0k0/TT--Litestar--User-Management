from typing import Annotated

from litestar import Controller, get, post, delete
from litestar.di import Provide
from litestar.params import Parameter
from litestar.pagination import OffsetPagination

from . import models, providers, schemas


class UsersController(Controller):
    """Контроллер для управления пользователями"""

    path = "/users"
    tags = ["users"]
    dependencies = {
        "user": Provide(providers.provide_user),
        "user_repo": Provide(providers.provide_user_repo),
    }
    return_dto = models.UserReadDTO

    @post(
        "/create",
        summary="Создание пользователя",
    )
    async def create_one(
        self,
        user_repo: providers.UserRepository,
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
        dependencies={
            "paginator": Provide(
                providers.UserOffsetPaginator,
                sync_to_thread=False,
            )
        },
    )
    async def get_all(
        self,
        paginator: providers.UserOffsetPaginator,
        limit: Annotated[
            int,
            Parameter(
                ge=1,
                le=100,
                description="Количество получаемых пользователей",
            ),
        ],
        offset: Annotated[
            int,
            Parameter(
                ge=0,
                default=0,
                description="Количество пропускаемых пользователя",
            ),
        ],
    ) -> OffsetPagination[models.User]:
        return await paginator(
            limit=limit,
            offset=offset,
        )

    @get(
        "/get",
        summary="Получение данных одного пользователя",
    )
    async def get_one(
        self,
        user: models.User,
    ) -> models.User:
        return user

    @post(
        "/update",
        summary="Обновление данных пользователя",
    )
    async def update_one(
        self,
        user: models.User,
        user_repo: providers.UserRepository,
        data: schemas.UserUpdate,
    ) -> models.User:
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
        user: models.User,
        user_repo: providers.UserRepository,
    ) -> None:
        await user_repo.delete(item_id=user.id)
