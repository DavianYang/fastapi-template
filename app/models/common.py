import datetime as dt
import uuid

from pydantic import UUID4, BaseModel, Field, validator


class DateTimeModelMixin(BaseModel):
    created_at: dt.datetime = Field(dt.datetime.now())
    updated_at: dt.datetime = None

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: dt.datetime) -> dt.datetime:
        return value or dt.datetime.now()


class IDModelMixin(BaseModel):
    id: UUID4 = Field(default_factory=lambda: str(uuid.uuid4()))


class AuthModelMixin(BaseModel):
    is_active: bool = Field(True)
    is_superuser: bool = Field(False)
