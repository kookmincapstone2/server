import json


def test_post_room_management(client, user):
    data = {
        'user_id': user.id,
        'title': 'test_room_title',
    }

    res = client.post('/api/room/management', data=data)
    assert res.status_code == 200


def test_get_room_management(client, user):
    data = {
        'room_id': user.room[0].id,
    }

    res = client.get('/api/room/management', query_string=data)
    assert res.status_code == 200


def test_put_room_management(client, user):
    data = {
        'user_id': user.id,
        'room_id': user.room[0].id,
        'title': user.room[0].title,
        'maximum_population': 60,
    }

    res = client.put('/api/room/management', data=data)
    assert res.status_code == 200


def test_delete_room_management(client, user):
    data = {
        'user_id': user.id,
        'room_id': user.room[0].id
    }

    res = client.get('/api/room/management', query_string=data)
    assert res.status_code == 200  # 가입된 방이 존재

    res = client.delete('/api/room/management', query_string=data)
    assert res.status_code == 200  # 방 삭제

    res = client.get('/api/room/management', query_string=data)
    assert res.status_code == 404  # 해당 방이 없음

    res = client.get('/api/room/member/management', query_string=data)
    assert res.status_code == 404  # 가입된 방이 없음


def test_post_room_member_management(client, user, basic_user):
    data = {
        'user_id': user.id,
        'invite_code': user.room[0].invite_code
    }

    res = client.post('/api/room/member/management', data=data)  # 방 가입
    assert res.status_code == 409

    data['user_id'] = basic_user.id
    res = client.post('/api/room/member/management', data=data)  # 방 가입
    assert res.status_code == 200


def test_get_room_member_management(client, user):
    data = {
        'user_id': user.id,
    }

    res = client.get('/api/room/member/management', query_string=data)
    assert res.status_code == 200


def test_delete_room_member_management(client, user):
    data = {
        'user_id': user.id,
        'room_id': user.room[0].id,
    }

    res = client.delete('/api/room/member/management', query_string=data)
    assert res.status_code == 200


def test_post_room_management(client, basic_user):  # maximum_population write test 2020-10-16
    data = {
        'user_id': basic_user.id,
        'title': 'test_room_title-2020-10-16',
        'maximum_population': 60,
    }

    res = client.post('/api/room/management', data=data)  # room 생성
    assert res.status_code == 200

    room_id = json.loads(res.data.decode())['room_id']  # 생성한 room id

    data = {
        'room_id': room_id
    }

    res = client.get('/api/room/management', query_string=data)
    assert res.status_code == 200
    assert json.loads(res.data.decode())['maximum_population'] == 60


def test_post_room_attendance_check(client, user):
    data = {
        'user_id': user.id,
        'room_id': user.room[0].id,
        'pass_num': '0123456789',
    }

    res = client.post('/api/room/attendance/check', data=data)
    assert res.status_code == 200


def test_put_room_attendance_check(client, user):
    data = {
        'user_id': user.id,
        'room_id': user.room[0].id,
        'pass_num': '0123456789'
    }

    res = client.post('/api/room/attendance/check', data=data)
    assert res.status_code == 200  # 출석코드 생성

    res = client.put('/api/room/attendance/check', data=data)
    assert res.status_code == 200  # 출석체크


def test_get_room_attendance_check(client, user):
    data = {
        'user_id': user.id,
        'room_id': user.room[0].id,
        'pass_num': '0123456789'
    }

    res = client.post('/api/room/attendance/check', data=data)
    assert res.status_code == 200  # 출석 코드 생성

    res = client.get('/api/room/attendance/check', query_string=data)
    assert res.status_code == 200


def test_get_room_member_all(client, user):  # 방에 가입된 모든 멤버를 보여줌
    data = {
        'room_id': user.room[0].id,
    }

    res = client.get('/api/room/member/all', query_string=data)
    assert res.status_code == 200
    assert json.loads(res.data.decode())['User'][0]['user_id'] == user.id


def test_post_delete_room_member_management(client, user, basic_user):
    data = {
        'user_id': basic_user.id,
        'invite_code': user.room[0].invite_code,
        'room_id': user.room[0].id,
    }

    res = client.post('/api/room/member/management', data=data)  # 유저가 방에 가입함
    assert res.status_code == 200

    res = client.delete('/api/room/member/management', query_string=data)  # 유저가 방에서 탈퇴함
    assert res.status_code == 200

    res = client.post('/api/room/member/management', data=data)  # 유저가 방에 다시 가입함
    assert res.status_code == 200


def test_attendance_check(client, user, basic_user):  # 출석체크 똑바로 뜨는지 확인 2020-12-05
    data = {
        'user_id': basic_user.id,
        'invite_code': user.room[0].invite_code,
        'room_id': user.room[0].id,
        'pass_num': 123456,
    }

    res = client.post('/api/room/member/management', data=data)  # 방에 멤버 추가
    assert res.status_code == 200

    data['user_id'] = user.id
    res = client.post('/api/room/attendance/check', data=data)  # 출석체크 생성
    assert res.status_code == 200

    res = client.get('/api/room/attendance/check', query_string=data)  # 출석 현황 검사
    assert res.status_code == 200
    assert len(json.loads(res.data.decode())['checked']) == 0

    data['user_id'] = basic_user.id
    res = client.put('/api/room/attendance/check', data=data)  # 출석체크
    assert res.status_code == 200

    data['user_id'] = user.id
    res = client.get('/api/room/attendance/check', query_string=data)  # 출석 현황 검사
    assert res.status_code == 200
    assert len(json.loads(res.data.decode())['checked']) == 1
