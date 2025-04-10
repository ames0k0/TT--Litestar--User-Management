from litestar import Router, get, post, delete

from src.schemas.users import UserCreatePayload, UserUpdatePayload


@post("/create")
async def create_one(payload: UserCreatePayload) -> str:
    return "OK"


@get("/get_all")
async def get_all() -> str:
    return "OK"


@get("/get")
async def get_one(id: int) -> str:
    return "OK"


@post("/update")
async def update_one(id: int, payload: UserUpdatePayload) -> str:
    return "OK"


@delete("/delete")
async def delete_one(id: int) -> None:
    pass


router = Router(
    path="/users",
    route_handlers=[
        create_one,
        get_all,
        get_one,
        update_one,
        delete_one,
    ],
)
