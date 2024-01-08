def test_user_login_successful(test_client, seed_db):
    obj = {
        'username': seed_db.username,
        'password': '1234@1234'
    }

    response = test_client.post(
        '/auth/login', json=obj, content_type='application/json')

    assert response.status_code == 200
    assert response.json['type'] == 'Bearer'
    assert response.json['access_token'] is not None
    assert response.json['refresh_token'] is not None


def test_user_login_failed(test_client, seed_db):
    obj = {
        'username': seed_db.username,
        'password': '1234@123'
    }

    response = test_client.post(
        '/auth/login', json=obj, content_type='application/json')

    assert response.status_code == 401
    assert response.json['msg'] == 'Usuário ou senha incorretos.'
