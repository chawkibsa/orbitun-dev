from sqlmodel import SQLModel, create_engine, Session, select



# Database setup
DATABASE_URL = "postgresql://orbitundev:orbitundev@localhost/orbitundevdb"
engine = create_engine(DATABASE_URL, echo=True)

# Database utilities
def get_session():
    with Session(engine) as session:
        yield session
