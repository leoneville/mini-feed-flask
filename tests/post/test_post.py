def test_create_post(test_client, seed_db, access_token):
    obj = {
        'text': 'Teste de criação de posts'
    }

    response = test_client.post('/posts', json=obj, headers=access_token)

    assert response.status_code == 201
    assert response.json['msg'] == 'Post criado com sucesso.'
