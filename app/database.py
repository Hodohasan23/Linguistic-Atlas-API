from sqlmodel import Session, create_engine
from typing import Generator
import os

def get_engine():
    url = os.environ.get("DATABASE_URL")
    return create_engine(url, echo=False)

def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session
