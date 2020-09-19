from sqlalchemy import Column, Integer, String

from db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    pw = Column(String, nullable=False)
    name = Column(String, nullable=False)
    student_id = Column(Integer, unique=True, nullable=False)
    phone = Column(Integer, unique=True, nullable=False)