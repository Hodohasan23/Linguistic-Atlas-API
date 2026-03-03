from sqlmodel import Session, create_engine
from typing import Generator

DATABASE_URL = "postgresql+psycopg://hodohasan:@localhost:5432/linguistic_atlas"

engine = create_engine(DATABASE_URL, echo=False)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
