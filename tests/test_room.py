def test_post_room_management(client, user):
    data = {
        'user_id': user.id,
        'title': 'test_room_title',
    }

    res = client.post('/api/room/management', data=data)
    assert res.status_code == 200
