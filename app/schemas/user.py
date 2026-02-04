from pydantic import BaseModel
from app.models.enums import Userrole


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class UserCreateAdmin(UserCreate):
    userrole: Userrole


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None


class UserRead(UserBase):
    id: int
    userrole: Userrole

    class Config:
        from_attributes = True


class UserInDB(UserRead):
    hashed_password: str


#For FastAPI + SQLAlchemy, response schemas must enable ORM mode.
"""from_attributes = True → allows SQLAlchemy model → schema conversion"""