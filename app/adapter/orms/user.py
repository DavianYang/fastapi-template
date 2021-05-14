import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.adapter.database import Base


class UserTable(Base):
    __tablename__ = "user"
    id = Column(UUID, primary_key=True)  # to modify later
    name = Column(String(length=60), nullable=False)
    email = Column(String(length=320), nullable=False)
    hashed_password = Column(String(length=72), nullable=False)
    photos = Column(String(length=255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime, nullable=True, default=dt.datetime.utcnow
    )  # change to true later
    updated_at = Column(DateTime, nullable=True, default=dt.datetime.utcnow)
    salt = Column(String(length=255), nullable=True)


users = UserTable.__table__
