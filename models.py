from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class urls(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index = True)
    short_url = Column(String, unique=True, index=True)
    user_id = Column(Integer,ForeignKey("Users.id"), index = True)


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
