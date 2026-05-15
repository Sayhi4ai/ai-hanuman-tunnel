from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./openclaw.db"

engine = create_engine(DATABASE_URL, echo=False)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
