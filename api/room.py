from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound, Forbidden, Unauthorized, Conflict

from api.models.room import *
from api.models.user import User
from settings.serialize import serialize
from settings.utils import api, check_data

app = Blueprint('room', __name__, url_prefix='/api')


@app.route('/room/management', methods=['POST'])
@api
def post_room_management(data, db):  # 방 생성
    req_list = ['user_id', 'title']
    check_data(data, req_list)

    master = db.query(User).filter(User.id == data['user_id']).first()  # 유저 객체를 가져옴

    if not master:  # 해당 유저가 존재 하지 않음
        raise NotFound

    new_room = Room(master_id=master.id,  # 새로운 방 생성
                    title=data['title'])

    if 'maximum_population' in data:  # 최대 인원을 제한했다면 정보 넣어줌
        Room.maximum_population = data['maximum_population']

    db.add(new_room)
    db.commit()

    new_room_member = RoomMember(room=new_room,  # 룸 멤버로 마스터를 생성함
                                 member_id=master.id)

    db.add(new_room_member)
    db.commit()

    return jsonify(serialize(new_room))


@app.route('/room/management', methods=['GET'])
@api
def get_room_management(data, db):  # 가입된 방을 검색함
    req_list = ['user_id']
    check_data(data, req_list)

    user = db.query(User).filter(User.id == data['user_id']).first()  # 유저 객체 가져옴

    if not user:  # 해당 유저가 존재하지 않음
        raise NotFound

    room_members = db.query(RoomMember).filter(RoomMember.member_id == user.id).all()  # 유저가 가입된 방을 모두 가져옴

    if not room_members:  # 가입된 방이 없음
        raise NotFound

    return jsonify(serialize(room_members))


@app.route('/room/management', methods=['PUT'])
@api
def put_room_management(data, db):  # 방 정보 수정
    req_list = ['user_id', 'room_id', 'title', 'maximum_population']
    check_data(data, req_list)

    user = db.query(User).filter(User.id == data['user_id']).first()  # 유저 객체 가져옴

    if not user:  # 해당 유저가 존재하지 않음
        raise NotFound

    room = db.query(Room).filter(Room.id == data['room_id']).first()

    if not room:  # 해당 방이 존재하지 않음
        raise NotFound

    if not user.id == room.master_id:  # 해당 유저가 마스터가 아니어서 수정 권한이 없음
        raise Forbidden

    room.title = data['title']
    room.maximum_population = data['maximum_population']

    db.commit()

    return jsonify(serialize(room))


@app.route('/room/management', methods=['DELETE'])
@api
def delete_room_management(data, db):  # 방 제거 함수
    req_list = ['user_id', 'room_id']
    check_data(data, req_list)

    room = db.query(Room).filter(Room.id == data['room_id']).first()

    if not room:  # 해당 방이 존재하지 않음
        raise NotFound

    if not str(room.master_id) == data['user_id']:  # 해당 유저가 마스터가 아니어서 권한이 없음
        raise Forbidden

    room.deleted_on = datetime.datetime.now()
    db.commit()

    return jsonify({})


@app.route('/room/member/management', methods=['POST'])
@api
def post_room_member_management(data, db):  # 방 가입 함수
    req_list = ['user_id', 'room_id', 'invite_code']
    check_data(data, req_list)

    user = db.query(User).filter(User.id == data['user_id']).first()
    if not user:  # 해당 유저 존재하지 않음
        raise NotFound

    room = db.query(Room).filter(Room.id == data['room_id']).first()
    if not room:  # 해당 방 존재하지 않음
        raise NotFound

    room_member = db.query(RoomMember).filter(RoomMember.room_id == data['room_id'],
                                              RoomMember.member_id == data['user_id'],
                                              RoomMember.deleted_on.is_(None), ).first()
    if room_member:  # 이미 가입된 방
        raise Conflict

    if not room.invite_code == data['invite_code']:  # 초대코드가 맞지 않음
        raise Unauthorized

    new_room_member = RoomMember(room_id=data['room_id'],
                                 member_id=data['user_id'], )
    db.add(new_room_member)
    db.commit()

    return jsonify({})


@app.route('/rom/member/management', methods=['DELETE'])
@api
def delete_room_member_management(data, db):
    req_list = ['user_id', 'room_id']
    check_data(data, req_list)

    user = db.query(User).filter(User.id == data['user_id']).first()
    if not user:  # 해당 유저 존재하지 않음
        raise NotFound

    room = db.query(Room).filter(Room.id == data['room_id']).first()
    if not room:  # 해당 방 존재하지 않음
        raise NotFound

    room_member = db.query(RoomMember).filter(RoomMember.room_id == data['room_id'],
                                              RoomMember.member_id == data['user_id'],
                                              RoomMember.deleted_on.is_(None), ).first()

    if not room_member:  # 가입되지 않은 방
        raise NotFound

    room_member.deleted_on = datetime.datetime.now()
    db.commit()

    return jsonify({})
