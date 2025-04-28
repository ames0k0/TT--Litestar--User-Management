from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar_granian import GranianPlugin

from src.core.config import settings
from src.routes import route_handlers


app = Litestar(
    path="/api/",
    route_handlers=route_handlers,
    plugins=[
        GranianPlugin(),
        settings.sqlalchemy.plugin,
    ],
    openapi_config=OpenAPIConfig(
        version="0.1.0",
        title="Тестовое задание",
        summary="REST API для управления пользователями",
    ),
)
