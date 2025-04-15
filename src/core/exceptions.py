from litestar import status_codes
from litestar.exceptions import HTTPException


class UserNotFound(HTTPException):
    def __init__(self, user_id: int):
        """Custom UserNotFound Exception

        Parameters
            user_id: int - Идентификатор пользователя
        """
        super().__init__(
            detail=f"No user found by id={user_id}",
            status_code=status_codes.HTTP_404_NOT_FOUND,
        )
