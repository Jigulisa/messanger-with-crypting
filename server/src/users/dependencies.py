from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession

from users.models.repositories import UserRepository


async def provide_user_repository(
    db_session: AsyncSession,
) -> UserRepository:
    return UserRepository(session=db_session)


dependencies = {
    "user_repository": Provide(provide_user_repository),
}
