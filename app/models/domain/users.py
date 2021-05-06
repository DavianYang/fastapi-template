from __future__ import annotations
from typing import Optional

from app.models.domain.rwmodel import RWModel
from app.models.common import DateTimeModelMixin, IDModelMixin
from app.services import security

class User(RWModel):
    name: str
    email: str
    photos: Optional[str]

    
class UserInDB(IDModelMixin, DateTimeModelMixin, User):
    salt: str = ""
    hashed_password: str = ""
    
    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)
    
    def hash_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)
    