from decimal import Decimal
from enum import IntEnum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class Permission(IntEnum):
    read_user_info = 1
    write_user_info = 2

    admin = read_user_info | write_user_info


class Role(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    permissions: Permission
    users: list["User"] = Relationship(back_populates="role")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    phone: Optional[str] = None
    credit_balance: Decimal = 0.0
    role_id: Optional[int] = Field(default=None, foreign_key="role.id")
    role: Optional[Role] = Relationship(back_populates="users")