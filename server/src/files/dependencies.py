from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession

from files.models.repositories import FileRepository


async def provide_file_repository(
    db_session: AsyncSession,
) -> FileRepository:
    return FileRepository(session=db_session)


dependencies = {
    "file_repository": Provide(provide_file_repository),
}
