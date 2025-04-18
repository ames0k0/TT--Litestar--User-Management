from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from litestar.params import Parameter
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from src.core import exceptions
from . import models


class UserRepository(SQLAlchemyAsyncRepository[models.User]):
    """User repository."""

    model_type = models.User


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """This provides the default User repository."""

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
