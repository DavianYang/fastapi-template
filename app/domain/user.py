from __future__ import annotations
from typing import Optional

from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr, SecretBytes
from pydantic.types import constr

class User(BaseModel):
    id: UUID
    name: constr(max_length=60)
    email: EmailStr
    photos: Optional[HttpUrl]
    password: SecretStr
    password_confirm: SecretBytes
    
    class Config:
        frozen=True
        orm_mode=True
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return other.id == self.id
    
    def __hash__(self) -> int:
        return hash(self.id)