from sqlmodel import SQLModel, create_engine, Session, select



# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)

# Database utilities
def get_session():
    with Session(engine) as session:
        yield session
