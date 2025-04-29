from typing import Annotated

from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session
from supabase import create_client, Client

from backend.app.core.config import get_settings

database_url = get_settings().database_url

engine = create_engine(database_url, echo=True)

session = Session(engine)


def get_db_session():
    with session:
        yield session


db_session = Annotated[Session, Depends(get_db_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


if __name__ == '__main__':
    create_db_and_tables()
# #run  python -m app.core.database once or import create_db_and_tables function in main router of the project

supabase_url: str = get_settings().supabase_url
supabase_key: str = get_settings().supabase_key
supabase: Client = create_client(supabase_url, supabase_key)
