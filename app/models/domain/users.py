from __future__ import annotations
from typing import Optional

from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr, SecretBytes
from pydantic.types import constr

from app.models.domain.rwmodel import RWModel
from app.models.common import DateTimeModelMixin, IDModelMixin

class User(RWModel):
    id: UUID
    name: constr(max_length=60)
    email: EmailStr
    photos: Optional[HttpUrl]
    
    class Config:
        frozen=True
        orm_mode=True
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return other.id == self.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    

class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    salt: str = ""
    hashed_password: SecretStr = ""
    
    def check_password(self, password: SecretStr) -> bool:
        pass
    
    def change_password(self, password: str) -> None:
        pass
    