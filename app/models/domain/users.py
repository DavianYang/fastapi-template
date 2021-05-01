from __future__ import annotations
from typing import Optional

from app.models.domain.rwmodel import RWModel
from app.models.common import DateTimeModelMixin, IDModelMixin

class User(RWModel):
    name: str
    email: str
    photos: Optional[str]

    
class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    salt: str = ""
    hashed_password: str = ""
    
    def check_password(self, password: str) -> bool:
        pass
    
    def change_password(self, password: str) -> None:
        pass
    