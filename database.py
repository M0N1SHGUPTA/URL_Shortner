from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

sqlite_file_name = "urls.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(
    sqlite_url, connect_args={"check_same_thread": False}
)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit= False ,autoflush=False, bind=engine)

#opens up a db connection that will be sandboxed and given to api route to perform db operations and closes it always usinf finally
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
