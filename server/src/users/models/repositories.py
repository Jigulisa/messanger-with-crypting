from litestar.plugins.sqlalchemy import repository

from users.models.orm import User


class UserRepository(repository.SQLAlchemyAsyncRepository[User]):
    model_type = User
