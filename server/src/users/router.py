from litestar import Router

from users.controllers import UsersController

router = Router(
    path="/users",
    route_handlers=[UsersController],
)
