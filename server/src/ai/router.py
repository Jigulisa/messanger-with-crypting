from litestar import Router

from ai.controllers import AIController

router = Router(
    path="/ai",
    route_handlers=[AIController],
)
