def test_post_authorization_signup(client):
    data = {
        'email': 'test@test.test',
        'pw': 'test123!@#',
        'name': 'tester',
        'student_id': 20153159,
        'phone': '01012341234',
    }

    res = client.post('/api/authorization/signup', data=data)
    assert res.status_code == 200


def test_get_authorization_email(client, user):
    data = {
        'email': user.email
    }

    res = client.get('/api/authorization/email', query_string=data)
    assert res.status_code == 409

    data['email'] = 'test@test.test1'
    res = client.get('/api/authorization/email', query_string=data)
    assert res.status_code == 200


def test_get_authorization_phone(client, user):
    data = {
        'phone': user.phone
    }

    res = client.get('/api/authorization/phone', query_string=data)
    assert res.status_code == 409

    data['phone'] = '01099999999'
    res = client.get('/api/authorization/phone', query_string=data)
    assert res.status_code == 200


def test_post_authorization_login(client, user):
    data = {
        'email': user.email,
        'pw': user.pw,
    }

    res = client.post('/api/authorization/login', data=data)
    assert res.status_code == 200
