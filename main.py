from litestar import Litestar

from src.routes import route_handlers


app = Litestar(
    path="/api/",
    route_handlers=route_handlers,
)
