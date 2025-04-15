from litestar import Litestar

from src.routes import route_handlers
from src.core.config import settings


app = Litestar(
    path="/api/",
    route_handlers=route_handlers,
    plugins=[settings.sqlalchemy.plugin],
)
