def test_post_authorization_signup(client):
    data = {
        'email': 'test@test.test',
        'pw': 'test123!@#',
        'name': 'tester',
        'student_id': 20153159,
        'phone': '01012341234',
        'rank': 'trash',
    }

    res = client.post('/api/authorization/signup', data=data)
    assert res.status_code == 400  # rank가 선생 또는 학생이 아님

    data['rank'] = 'teacher'
    res = client.post('/api/authorization/signup', data=data)
    assert res.status_code == 200

    res = client.post('/api/authorization/signup', data=data)  # 이미 존재하는 이메일 또는 핸드폰번호를 입력한 경우
    assert res.status_code == 401


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
