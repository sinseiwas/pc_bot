from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
    )
from sqlalchemy import (
    BigInteger
)
from db.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)
    tg_username: Mapped[str | None]
    tg_fullname: Mapped[str]
    fullname: Mapped[str]
    phone_number: Mapped[str]
    vk_link: Mapped[str]

    requests: Mapped[list["Request"]] = relationship("Request", back_populates="user") # type: ignore