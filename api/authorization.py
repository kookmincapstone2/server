from flask import Blueprint, jsonify
from werkzeug.exceptions import BadRequest, Conflict, Unauthorized

from api.models.user import User
from settings.serialize import serialize
from settings.utils import api, check_data

app = Blueprint('auth', __name__, url_prefix='/api')


@app.route('/authorization/signup', methods=['POST'])
@api
def post_authorization_signup(data, db):
    req_list = ['email', 'pw', 'name', 'student_id', 'phone', 'rank']
    check_data(data, req_list)

    user = db.query(User).filter(User.email == data['email']).first()
    if user:  # 이미 존재하는 이메일
        raise Unauthorized

    user = db.query(User).filter(User.phone == data['phone']).first()
    if user:  # 이미 존재하는 핸드폰번호
        raise Unauthorized

    if not data['rank'] == 'teacher' and not data['rank'] == 'student':  # 학생 또는 선생이 아닐 경우 잘못된 요청
        raise BadRequest

    new_user = User(email=data['email'],
                    pw=data['pw'],
                    name=data['name'],
                    student_id=data['student_id'],
                    phone=data['phone'],
                    rank=data['rank'])  # 새로운 유저 생성

    db.add(new_user)
    db.commit()

    return jsonify({})


@app.route('/authorization/email', methods=['GET'])
@api
def get_authorization_email(data, db):
    req_list = ['email']
    check_data(data, req_list)

    user = db.query(User).filter(User.email == data['email']).first()
    if user:  # 이미 사용중인 이메일
        raise Conflict

    return jsonify({})


@app.route('/authorization/phone', methods=['GET'])
@api
def get_authorization_phone(data, db):
    req_list = ['phone']
    check_data(data, req_list)

    user = db.query(User).filter(User.phone == data['phone']).first()
    if user:  # 이미 사용중인 전화번호
        raise Conflict

    return jsonify({})


@app.route('/authorization/login', methods=['POST'])
@api
def post_authorization_login(data, db):
    req_list = ['email', 'pw']
    check_data(data, req_list)

    user = db.query(User).filter(User.email == data['email'],
                                 User.pw == data['pw']).first()
    if not user:  # email 또는 pw이 틀림
        return jsonify({'reason': 'login fail'}), 404

    return jsonify(serialize(user))
