from sqlmodel import Field, SQLModel


class Secrets(SQLModel, table=True):
    key: str = Field(primary_key=True)
    name: str | None = None
    project: str | None = None
    expiration_date: str | None = None


