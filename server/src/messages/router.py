from litestar import Router

from messages.controllers import messages
from messages.dependencies import dependencies

router = Router(
    path="/messages",
    route_handlers=[messages],
    dependencies=dependencies,
)
