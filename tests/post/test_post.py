def test_create_post(test_client, seed_db, access_token):
    obj = {
        'text': 'Teste de criação de posts'
    }

    response = test_client.post('/posts', json=obj, headers=access_token)

    assert response.status_code == 201
    assert response.json['msg'] == 'Post criado com sucesso.'


def test_update_post(test_client, seed_db, access_token, seed_post):
    obj = {
        'text': 'Teste de atualizacao de post'
    }

    response = test_client.put('/posts/1', json=obj, headers=access_token)

    assert response.status_code == 200
    assert response.json['msg'] == 'Post atualizado com sucesso.'


def test_denied_update_post(test_client, seed_db, access_token, seed_post):
    obj = {
        'text': 'Teste de atualização negada de post'
    }

    response = test_client.put('/posts/2', json=obj, headers=access_token)

    assert response.status_code == 403
    assert response.json['msg'] == 'Você não tem permissão para editar este post.'


def test_delete_post(test_client, seed_db, access_token, seed_post):
    response = test_client.delete('/posts/1', headers=access_token)

    assert response.status_code == 200
    assert response.json['msg'] == 'Post deletado com sucesso.'
