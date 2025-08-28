from litestar.plugins.sqlalchemy import repository

from files.models.orm import File


class FileRepository(repository.SQLAlchemyAsyncRepository[File]):
    model_type = File
