from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey
from db.db import Base
from datetime import datetime


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    work_type: Mapped[str]
    nine_photos: Mapped[bool]
    info: Mapped[str]
    event_name: Mapped[str]
    start_datetime: Mapped[datetime]
    end_datetime: Mapped[datetime]
    place: Mapped[str]
    phone_number: Mapped[str]
    event_link: Mapped[str]
    organizer_fullname: Mapped[str]
    organizer_vk_link: Mapped[str]
    status: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="requests") # type: ignore