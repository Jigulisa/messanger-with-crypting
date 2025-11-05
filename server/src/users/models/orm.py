from litestar.plugins.sqlalchemy import base
from sqlalchemy import Index, func
from sqlalchemy.orm import Mapped, mapped_column


class User(base.UUIDv7AuditBase):
    dsa_public_key: Mapped[str] = mapped_column()
    kem_public_key: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int | None]
    full_name: Mapped[str | None]
    gender_male: Mapped[bool | None]
    gender_female: Mapped[bool | None]
    voleyball: Mapped[bool | None]
    programming: Mapped[bool | None]
    ml: Mapped[bool | None]
    algorythms: Mapped[bool | None]
    rock: Mapped[bool | None]
    drawing: Mapped[bool | None]
    art: Mapped[bool | None]
    manga: Mapped[bool | None]
    anime: Mapped[bool | None]
    politics: Mapped[bool | None]
    diy: Mapped[bool | None]
    style: Mapped[bool | None]
    hairstyling: Mapped[bool | None]
    knitting: Mapped[bool | None]
    series: Mapped[bool | None]
    frontend: Mapped[bool | None]
    doing_music: Mapped[bool | None]
    reading: Mapped[bool | None]
    other_hobby: Mapped[bool | None]

    __table_args__ = (
        Index("idx_user_dsa_public_key_md5", func.md5(dsa_public_key), unique=True),
        Index("idx_user_kem_public_key_md5", func.md5(kem_public_key), unique=True),
    )
