from litestar import Router

from files.controllers import FilesController
from files.dependencies import dependencies

router = Router(
    path="/files",
    route_handlers=[FilesController],
    dependencies=dependencies,
)
