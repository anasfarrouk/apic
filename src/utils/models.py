from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String, CheckConstraint
from pydantic import field_validator


class Secrets(SQLModel, table=True):
    __table_args__ = (CheckConstraint("name <> ''", name="ck_secrets_name_not_empty"),)
    key: str = Field(primary_key=True)
    name: str = Field(..., sa_column=Column(String, unique=True, nullable=False))
    project: str | None = None
    expiration_date: str | None = None

    @field_validator("name")
    def name_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("name must not be empty")
        return v

