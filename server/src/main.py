from typing import Self

from litestar import Litestar
from litestar.channels import ChannelsPlugin
from litestar.channels.backends.memory import MemoryChannelsBackend
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
    base,
)

from files.router import router as files_router
from messages.router import router as messages_router
from users.middleware import middleware as users_middleware


class OnSturtup:
    sqlalchemy_config = SQLAlchemyAsyncConfig(
        connection_string="sqlite+aiosqlite:///database.sqlite",
        session_config=AsyncSessionConfig(expire_on_commit=False),
    )

    async def __call__(self: Self) -> None:
        async with self.sqlalchemy_config.get_engine().begin() as connection:
            await connection.run_sync(base.UUIDv7AuditBase.metadata.drop_all)
            await connection.run_sync(base.UUIDv7AuditBase.metadata.create_all)


app = Litestar(
    route_handlers=[files_router, messages_router],
    on_startup=[OnSturtup()],
    plugins=[
        ChannelsPlugin(backend=MemoryChannelsBackend(), channels=["messages_channel"]),
        SQLAlchemyInitPlugin(config=OnSturtup.sqlalchemy_config),
    ],
    middleware=users_middleware,
)


#               __
# /\  /\ |---- /  \ |    |
# | \/ | |     |  | |    |
# |    | |---- |  | | /\ |
# |    | |---- \__/ \/  \/

# буду ml'щиком
