from typing import Annotated, cast

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import ScalarResult
from litestar.params import Parameter
from litestar.pagination import AbstractAsyncOffsetPaginator
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from src.core import exceptions
from . import models


class UserRepository(SQLAlchemyAsyncRepository[models.User]):
    """User repository"""

    model_type = models.User


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """This provides the default User repository"""

    return UserRepository(session=db_session)


async def provide_user(
    id: Annotated[
        int,
        Parameter(ge=1, description="Идентификатор пользователя"),
    ],
    user_repo: UserRepository,
) -> models.User:
    """This provides a `User` for a given `id`"""

    user = await user_repo.get_one_or_none(id=id)
    if not user:
        raise exceptions.UserNotFound(user_id=id)

    return user


class UserOffsetPaginator(AbstractAsyncOffsetPaginator[models.User]):
    """User paginator"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_total(self) -> int:
        return cast(
            "int",
            await self.db_session.scalar(
                select(
                    func.count(
                        models.User.id,
                    )
                )
            ),
        )

    async def get_items(self, limit: int, offset: int) -> list[models.User]:
        users: ScalarResult = await self.db_session.scalars(
            select(models.User).slice(offset, offset + limit)
        )
        return list(users.all())
