from datetime import date, datetime

from models import User


def test_get_user_by_id(test_client, seed_db, access_token):
    response = test_client.get('/users/1', headers=access_token)

    assert response.status_code == 200
    assert response.json['id'] == seed_db.id
    assert response.json['username'] == seed_db.username
    assert response.json['birthdate'] == seed_db.birthdate.isoformat()
    assert response.json['created_at'] == seed_db.created_at.isoformat()


def test_get_user_by_id_not_found(test_client, seed_db, access_token):
    response = test_client.get('/users/99999', headers=access_token)

    assert response.status_code == 404
    assert response.json['msg'] == 'Usuário não encontrado.'


def test_get_all_users(test_client, seed_db, access_token):
    response = test_client.get('/users', headers=access_token)

    assert response.status_code == 200
    assert response.json[0]['id'] == seed_db.id
    assert response.json[0]['username'] == seed_db.username
    assert response.json[0]['birthdate'] == seed_db.birthdate.isoformat()
    assert response.json[0]['created_at'] == seed_db.created_at.isoformat()


def test_post_user(test_client):
    data = {
        "username": "leoneville.dev",
        "email": "leoneville.dev@gmail.com",
        "birthdate": "1998-01-21",
        "password": '1234@1234'
    }

    response = test_client.post(
        '/users', json=data, content_type='application/json')

    user = User.query.filter_by(username=data['username']).first()

    assert response.status_code == 201
    assert response.json['msg'] == 'Usuário criado com sucesso.'
    assert user.username == data['username']
    assert user.email == data['email']
    assert user.birthdate == date.fromisoformat(data['birthdate'])


def test_post_user_username_conflict(test_client, seed_db):
    data = {
        "username": "neville_bg",
        "email": "leoneville.dev@gmail.com",
        "password": "1234@1234"
    }

    response = test_client.post(
        '/users', json=data, content_type='application/json')

    assert response.status_code == 409
    assert response.json['msg'] == 'Username não disponível.'


def test_post_user_email_conflict(test_client, seed_db):
    data = {
        "username": "leoneville.dev",
        "email": "neville_bg@hotmail.com",
        "password": "1234@1234"
    }

    response = test_client.post(
        '/users', json=data, content_type='application/json')

    assert response.status_code == 409
    assert response.json['msg'] == 'Email já cadastrado.'


def test_put_user(test_client, seed_db, access_token):
    data = {
        "username": "lacoxt",
        "email": "lacoxt@gmail.com",
        "birthdate": datetime.now().date().isoformat()
    }
    response = test_client.put(
        '/users', json=data, content_type='application/json', headers=access_token)

    user = User.query.filter_by(username=data['username']).first()

    assert response.status_code == 200
    assert response.json['msg'] == 'Usuário atualizado com sucesso.'
    assert user.username == data['username']
    assert user.email == data['email']
    assert user.birthdate == date.fromisoformat(data['birthdate'])


def test_put_user_username_conflict(test_client, seed_db, seed_more_db, access_token):
    data = {
        "username": "leoneville.dev",
        "email": "lacoxt@gmail.com"
    }

    response = test_client.put(
        '/users', json=data, content_type='application/json', headers=access_token)

    assert response.status_code == 409
    assert response.json['msg'] == 'Username não disponível.'


def test_put_user_email_conflict(test_client, seed_db, seed_more_db, access_token):
    data = {
        "username": "lacoxt",
        "email": "leoneville.dev@gmail.com"
    }

    response = test_client.put(
        '/users', json=data, content_type='application/json', headers=access_token)

    assert response.status_code == 409
    assert response.json['msg'] == 'Email já cadastrado.'


def test_delete_user(test_client, seed_db, access_token):
    response = test_client.delete('/users/1', headers=access_token)

    assert response.status_code == 200
    assert response.json['msg'] == 'Usuário deletado com sucesso.'


def test_delete_user_not_found(test_client, seed_db, access_token):
    response = test_client.delete('users/99999', headers=access_token)

    assert response.status_code == 404
    assert response.json['msg'] == 'Usuário não encontrado.'
