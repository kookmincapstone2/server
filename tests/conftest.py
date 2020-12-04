from pytest import fixture
from sqlalchemy import create_engine

from api.models.room import Room, RoomMember
from api.models.user import User
from db import Base, Database
from settings.settings import DB_URI, NAME, PASSWOLRD, DB_PORT, HOST_ADDR
from settings.wsgi import create_wsgi

app = create_wsgi()


@fixture()
def client(init_database):  # pytest용 클라이언트
    return app.test_client()


@fixture(scope='session')
def database():  # pytest용 일회용 데이터베이스
    engine = create_engine(f'postgresql://postgres:{PASSWOLRD}@{HOST_ADDR}:{DB_PORT}',
                           connect_args={'connect_timeout': 10})
    conn = engine.connect()
    conn.execute("COMMIT")

    conn.execute(f"DROP DATABASE IF EXISTS {NAME}")
    conn.execute("COMMIT")
    conn.execute(f"CREATE DATABASE {NAME}")
    conn.execute("COMMIT")
    conn.close()


@fixture()
def init_database(database):
    engine = create_engine(DB_URI, connect_args={'connect_timeout': 10})
    Base.metadata.create_all(engine)


ID_NUM = 1234


@fixture()
def user():
    global ID_NUM
    ID_NUM = ID_NUM + 1
    with Database() as db:
        new_user = User(
            email=f'master{ID_NUM}@master.master',
            pw='master123!@#',
            name=f'teacher{ID_NUM}',
            student_id=ID_NUM,
            phone=f'0100000{ID_NUM}',
            rank='teacher',
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.expunge(new_user)

        new_room = Room(
            master_id=new_user.id,
            title=f'test_title{ID_NUM}',
        )

        db.add(new_room)
        db.commit()
        db.refresh(new_room)
        db.expunge(new_room)

        new_room_member = RoomMember(
            room_id=new_room.id,
            member_id=new_user.id,
        )

        db.add(new_room_member)
        db.commit()
        db.refresh(new_room_member)
        db.expunge(new_room_member)

        new_room.room_member.append(new_room_member)
        new_user.room.append(new_room)

        return new_user


@fixture()
def basic_user():
    global ID_NUM
    ID_NUM = ID_NUM + 1
    with Database() as db:
        new_user = User(
            email=f'master{ID_NUM}@master.master',
            pw='master123!@#',
            name=f'student{ID_NUM}',
            student_id=ID_NUM,
            phone=f'0100000{ID_NUM}',
            rank='student',
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db.expunge(new_user)

        return new_user
