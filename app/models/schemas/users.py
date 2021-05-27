from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.domain.users import User
from app.models.schemas.rwschema import RWSchema


class UserInLogin(RWSchema):
    email: EmailStr
    password: str


class UserInCreate(RWSchema):
    name: str
    email: EmailStr
    password: str


class UserInUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    image: Optional[str] = None


class UserWithToken(User):
    token: str


class UserInResponse(RWSchema):
    user: UserWithToken
