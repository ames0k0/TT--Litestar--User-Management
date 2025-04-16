from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from src.routes import route_handlers
from src.core.config import settings


app = Litestar(
    path="/api/",
    route_handlers=route_handlers,
    plugins=[
        settings.sqlalchemy.plugin,
    ],
    openapi_config=OpenAPIConfig(
        version="1.0.0",
        title="Тестовое задание",
        summary="REST API для управления пользователями",
    ),
)
