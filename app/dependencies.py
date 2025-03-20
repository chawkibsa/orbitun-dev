from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv


# Database setup                                                                             
load_dotenv()  # Load environment variables from .env

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")
engine = create_engine(DATABASE_URL, echo=True)

# Database utilities
def get_session():
    with Session(engine) as session:
        yield session
