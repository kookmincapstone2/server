import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship

from db import Base


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, autoincrement=True)
    master = relationship('User', back_populates='room')  # 방 생성자
    created_on = Column(DateTime, nullable=False, unique=False, default=datetime.datetime.now)  # 생성 날짜
    deleted_on = Column(DateTime, nullable=True, unique=False)  # 제거 날짜
    maximum_population = Column(Integer, nullable=True, unique=False)
    room_member = relationship('RoomMember', back_populates='room')


class RoomMember(Base):
    __tablename__ = 'room_member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room = relationship('Room', back_populates='room_member')
    user = relationship('User', back_populates='room')
