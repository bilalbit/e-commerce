from sqlmodel import create_engine, SQLModel, Session

from app.modules import * ##importing all models
from app.core.config import get_settings

database_url = get_settings().database_url


engine = create_engine(database_url, echo=True)
# engine = create_engine(database_url)

session = Session(engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
if __name__ == '__main__':
    create_db_and_tables()
# #run  python -m app.core.database once or import create_db_and_tables function in main router of the project

