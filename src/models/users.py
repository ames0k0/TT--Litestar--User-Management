from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy.orm import Mapped

from litestar.contrib.sqlalchemy.dto import SQLAlchemyDTO, SQLAlchemyDTOConfig


class User(BigIntAuditBase):
    """User model with auto-incrementing ID and audit fields.

    Attributes:
        name: User name
        surname: User surname
        password: User password
        created_at: Timestamp of creation (from BigIntAuditBase)
        updated_at: Timestamp of last update (from BigIntAuditBase)
    """

    name: Mapped[str]
    surname: Mapped[str]
    password: Mapped[str]


class UserDTO(SQLAlchemyDTO[User]):
    """User DTO"""

    config = SQLAlchemyDTOConfig(exclude={"password"})
