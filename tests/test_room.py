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

    res = client.delete('/api/room/management', query_string=data)
    assert res.status_code == 200


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
