from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref

from db import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    pw = Column(String, nullable=False)
    name = Column(String, nullable=False)
    student_id = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    room = relationship('Room', lazy='subquery', backref=backref('user'))
    rank = Column(String, unique=False, nullable=False)  # 선생 또는 학생
