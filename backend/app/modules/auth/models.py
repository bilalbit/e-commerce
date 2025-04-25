import uuid

from sqlmodel import SQLModel, Field

from app.modules.users.models import RoleType


class UserSchema(SQLModel):
    id: uuid.UUID
    username: str = Field(min_length=3)
    role: RoleType


class Token(SQLModel):
    access_token: str
    token_type: str