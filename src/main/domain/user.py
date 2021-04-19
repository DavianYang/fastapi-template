from __future__ import annotations
from dataclasses import dataclass
from typing import List, NewType, Optional

UserId = NewType("UserId", int)

class User:
    def __init__(
        self,
        id: UserId,
        name: str,
        email: str,
        photo: str,
        password: str,
        password_confirm: str
    ) -> None:
        self.name = name
        self.email = email
        self.photo = photo
        self.password = password
        self.password_confirm = password_confirm
        
    def __repr__(self) -> str:
        return f"<User {self.id}>"
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, User):
            return False
        return o.id == self.id
    
    def __hash__(self) -> int:
        return hash(self.id)