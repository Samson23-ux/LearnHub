from .conftest import fake_data

def test_get_stats(test_client, enrol_create):
    _, admin, *_ = enrol_create

    response = test_client.get(
        '/admin/stats/',
        headers={
            'Authorization': admin.json()['data']['token']
        }
    )

    assert 'users' in response.json()['data']
    assert 'courses' in response.json()['data']
    assert 'enrolments' in response.json()['data']

def test_delete_account(test_client, account_sign_in):
    admin, *_ = account_sign_in
    test_client.request(
        'DELETE',
        '/admin/users/3/',
        data={
            'password': fake_data['password']
        },
        headers={
            'Authorization': admin.json()['data']['token']
        }
    )

    response = test_client.get(
        '/users/gasmine rabbit/',
        headers={
            'Authorization': admin.json()['data']['token']
        }
    )

    assert response.status_code == 404
