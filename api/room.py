from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Conflict, Forbidden

from api.models.room import *
from api.models.user import User
from settings.serialize import serialize
from settings.utils import api

app = Blueprint('room', __name__, url_prefix='/api')


@app.route('/room/management', methods=['POST'])
@api
def post_room_management(data, db):  # 방 생성
    req_list = ['user_id', 'title']
    for i in req_list:
        if i not in data:
            raise BadRequest

    master = db.query(User).filter(User.id == data['user_id']).first()  # 유저 객체를 가져옴

    if not master:  # 해당 유저가 존재 하지 않음
        raise Conflict

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
    for i in req_list:
        if i not in data:
            raise BadRequest

    user = db.query(User).filter(User.id == data['user_id']).first()  # 유저 객체 가져옴

    if not user:  # 해당 유저가 존재하지 않음
        raise Conflict

    room_members = db.query(RoomMember).filter(RoomMember.member_id == user.id).all()  # 유저가 가입된 방을 모두 가져옴

    if not room_members:  # 가입된 방이 없음
        raise NotFound

    return jsonify(serialize(room_members))


@app.route('/room/management', methods=['PUT'])
@api
def put_room_management(data, db):  # 방 정보 수정
    req_list = ['user_id', 'room_id', 'title', 'maximum_population']
    for i in req_list:
        if i not in data:
            raise BadRequest

    user = db.query(User).filter(User.id == data['user_id']).first()  # 유저 객체 가져옴

    if not user:  # 해당 유저가 존재하지 않음
        raise Conflict

    room = db.query(Room).filter(Room.id == data['room_id']).first()

    if not room:  # 해당 방이 존재하지 않음
        raise Conflict

    if not user.id == room.master_id:  # 해당 유저가 마스터가 아니어서 수정 권한이 없음
        raise Forbidden

    room.title = data['title']
    room.maximum_population = data['maximum_population']

    db.commit()

    return jsonify(serialize(room))


@app.route('/room/management', methods=['DELETE'])
@api
def delete_room_management(data, db):
    req_list = ['user_id', 'room_id']
    for i in req_list:
        if i not in data:
            raise BadRequest

    room = db.query(Room).filter(Room.id == data['room_id']).first()

    if not room:  # 해당 방이 존재하지 않음
        raise Conflict

    if not str(room.master_id) == data['user_id']:  # 해당 유저가 마스터가 아니어서 권한이 없음
        raise Forbidden

    db.delete(room)
    db.commit()

    return jsonify({})
