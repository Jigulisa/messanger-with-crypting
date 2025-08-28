from typing import Self

from litestar import Controller, Request, get

from users.models.repositories import UserRepository


class UsersController(Controller):
    @get("/kem")
    async def create_chat(
        self: Self,
        request: Request,
        username: str,
        user_repository: UserRepository,
    ) -> str:
        return (await user_repository.get_one(username=username)).kem_public_key
