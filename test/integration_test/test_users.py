from .conftest import fake_data

def test_get_users(test_client, account_sign_in):
    user, *_ = account_sign_in
    response = test_client.get(
        '/users/',
        headers={
            'Authorization': user.json()['data']['token']
        }
    )

    assert response.status_code == 200
    assert len(response.json()['data']) >= 1

def test_get_user(test_client, account_sign_in):
    user, *_ = account_sign_in
    response = test_client.get(
        '/users/jojojojo/',
        headers={
            'Authorization': user.json()['data']['token']
        }
    )

    assert response.status_code == 200
    assert response.json()['data']['username'] == fake_data['username']

def test_update_user(test_client, account_sign_in):
    user, *_ = account_sign_in
    username = 'jojosamson22'

    response = test_client.patch(
        '/users/1/',
        json={
            'username': username,
            'curr_password': fake_data['password']
        },
        headers={
            'Authorization': user.json()['data']['token']
        }
    )

    assert response.status_code == 200
    assert response.json()['data']['username'] == username

def test_update_password(test_client, account_sign_in):
    new_password ='hdhdhdhdhdhdh347'
    user, *_ = account_sign_in

    test_client.patch(
        '/users/1/update-password',
        json={
            'curr_password': fake_data['password'],
            'new_password': new_password
        },
        headers={
            'Authorization': user.json()['data']['token']
        }
    )

    response = test_client.post(
        '/auth/sign-in/1/',
        json={
            'email': fake_data['email'],
            'password': new_password
        }
    )

    assert response.status_code == 200
    assert 'token' in response.json()['data']
