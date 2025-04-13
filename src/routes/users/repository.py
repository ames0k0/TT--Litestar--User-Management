from sqlalchemy.ext.asyncio import AsyncSession
from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository

from . import models


class UserRepository(SQLAlchemyAsyncRepository[models.User]):
    """User repository."""

    model_type = models.User


async def provide_user_repo(db_session: AsyncSession) -> UserRepository:
    """This provides the default User repository."""

    return UserRepository(session=db_session)
