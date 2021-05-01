from __future__ import annotations
from typing import Optional

from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr, SecretBytes
from pydantic.types import constr

from app.models.domain.rwmodel import RWModel
from app.models.common import DateTimeModelMixin, IDModelMixin

class User(RWModel):
    name: str
    email: str
    photos: Optional[HttpUrl]

    
class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    salt: str = ""
    hashed_password: SecretStr = ""
    
    def check_password(self, password: SecretStr) -> bool:
        pass
    
    def change_password(self, password: str) -> None:
        pass
    