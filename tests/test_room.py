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


def test_post_room_member_managemet(client, user):
    data = {

    }
    res = client.post('/api/room/member/management', data=data)
    assert res.status_code == 400
