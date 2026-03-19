from sqlmodel import SQLModel, create_engine


sqlite_db = "sqlite:///mybase.db"

engine = create_engine(sqlite_db, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

