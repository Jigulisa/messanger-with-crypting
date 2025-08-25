from typing import Self

from litestar import Controller, Request, delete, get, post
from litestar.exceptions.http_exceptions import (
    NotFoundException,
)

from files.models.dto import FileProperties
from files.models.repositories import FileRepository


class FilesController(Controller):
    @get("/names")
    async def get_file_names(
        self: Self,
        request: Request,
        file_repository: FileRepository,
    ) -> list[str]:
        return [file.name for file in await file_repository.list(owner=request.user)]

    @get("/download")
    async def download_file(
        self: Self,
        request: Request,
        name: str,
        file_repository: FileRepository,
    ) -> bytes:
        file = await file_repository.get_one_or_none(owner=request.user, name=name)
        if file is None:
            raise NotFoundException
        return file.data

    @post("/rename")
    async def rename_file(
        self: Self,
        request: Request,
        old: str,
        new: str,
        file_repository: FileRepository,
    ) -> str:
        file, found = await file_repository.get_and_update(
            owner=request.user,
            name=old,
            attribute_names={"name": new},
        )
        if found:
            return file.name
        raise NotFoundException

    @get("/properties")
    async def get_file_properties(
        self: Self,
        request: Request,
        name: str,
        file_repository: FileRepository,
    ) -> FileProperties:
        file = await file_repository.get_one_or_none(owner=request.user, name=name)
        if file is None:
            raise NotFoundException
        return FileProperties(
            name=file.name,
            owner=file.owner.public_key,
            size=len(file.data),
            created_at=file.created_at,
            updated_at=file.updated_at,
        )

    @delete("/delete")
    async def delete_file(
        self: Self,
        request: Request,
        name: str,
        file_repository: FileRepository,
    ) -> None:
        await file_repository.delete_where(owner=request.user, name=name)


"""
@get("/get_file_names")
def get_file_names(user: str) -> Response:
    folder_path = Path(__file__).parent / f"storage/{user}"
    if not folder_path.exists():
        folder_path.mkdir()
        resp = AllFileNamesModel(names=[])
        return Response(content=resp, status_code=HTTP_200_OK)

    files = [file.name for file in folder_path.iterdir()]
    resp = AllFileNamesModel(names=files)
    return Response(content=resp, status_code=HTTP_200_OK)


@get("/download_file")
async def download_file(user: str, name: str) -> Response:
    path = Path(__file__).parent / f"storage/{user}/{name}"
    content = path.read_bytes()
    resp = DownloadFileModel(data=content)
    return Response(content=resp, status_code=HTTP_200_OK)


@post("/rename")
def rename(user: str, old: str, new: str) -> Response:
    old_file = Path(__file__).parent / f"storage/{user}/{old}"
    new_file = Path(__file__).parent / f"storage/{user}/{new}"
    try:
        old_file.rename(new_file)
    except Exception:
        resp = RenameModel(message="Error. Try again.")
        return Response(content=resp, status_code=HTTP_400_BAD_REQUEST)

    resp = RenameModel(message="Ok.")
    return Response(content=resp, status_code=HTTP_200_OK)


@get("/get_file_properties")
def get_file_properties(user: str, name: str) -> Response:
    path = Path(__file__).parent / f"storage/{user}/{name}"
    try:
        stats = path.stat()
        birth_datetime = datetime.fromtimestamp(
            stats.st_birthtime,
            ZoneInfo("Europe/Moscow"),
        )
        last_datetime = datetime.fromtimestamp(
            stats.st_atime,
            ZoneInfo("Europe/Moscow"),
        )
        resp = GetFilePropertiesModel(
            name=name.split(".")[0],
            load_time=birth_datetime,
            size=stats.st_size,
            last_touched=last_datetime,
        )
        return Response(content=resp, status_code=HTTP_200_OK)
    except Exception:
        return Response(content=None, status_code=HTTP_404_NOT_FOUND)


@post("/delete_file")
def delete_file(user: str, name: str) -> Response:
    path = Path(__file__).parent / f"storage/{user}/{name}"
    if not path.exists():
        resp = DeleteModel(message="Error occured.")
        return Response(content=resp, status_code=HTTP_404_NOT_FOUND)
    path.unlink()
    resp = DeleteModel(message="File deleted.")
    return Response(content=resp, status_code=HTTP_200_OK)
"""
