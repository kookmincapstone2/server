import datetime
import uuid

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import UUIDType

from db import Base


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, autoincrement=True)
    master_id = Column(Integer, ForeignKey('user.id'))  # 방 생성자
    title = Column(String, nullable=False, unique=False)  # room title
    created_on = Column(DateTime, nullable=False, unique=False, default=datetime.datetime.now)  # 생성 날짜
    deleted_on = Column(DateTime, nullable=True, unique=False)  # 제거 날짜
    maximum_population = Column(Integer, nullable=True, unique=False)
    room_member = relationship('RoomMember', lazy='subquery', backref=backref('room'))
    invite_code = Column(UUIDType, nullable=False, unique=True, default=uuid.uuid4)  # 방 초대 코드


class RoomMember(Base):
    __tablename__ = 'room_member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('room.id'))
    member_id = Column(Integer, ForeignKey('user.id'))
    created_on = Column(DateTime, nullable=False, unique=False, default=datetime.datetime.now)  # 생성 날짜
    deleted_on = Column(DateTime, nullable=True, unique=False)  # 제거 날짜


class AttendanceCheck(Base):
    __tablename__ = 'attendance_check'

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_id = Column(Integer, ForeignKey('room.id'))
    created_on = Column(DateTime, nullable=False, unique=False, default=datetime.datetime.now)  # 생성 날짜
    is_checked = Column(Boolean, nullable=False, unique=False, default=False)  # 출석 체크 여부
    pass_num = Column(String, nullable=False, unique=False)  # 출석 비밀번호
