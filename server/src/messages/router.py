from litestar import Router

from messages.controllers import ChatController, messages
from messages.dependencies import dependencies

router = Router(
    path="/messages",
    route_handlers=[messages, ChatController],
    dependencies=dependencies,
)
