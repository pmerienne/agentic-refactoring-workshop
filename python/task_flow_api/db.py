from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def init_db():
    # Import all models to ensure they're registered with SQLModel metadata
    from task_flow_api.model import Task  # noqa: F401

    SQLModel.metadata.create_all(engine)


def create_session():
    return Session(engine)
