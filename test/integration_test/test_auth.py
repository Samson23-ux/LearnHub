import pytest_asyncio
from .conftest import fake_data

def test_sign_up(test_client, account_create):
    account = account_create

    assert account.status_code == 201
    assert 'id' in account.json()['data']
    assert fake_data['username'] == account.json()['data']['username']

def test_sign_in(test_client, account_sign_in):
    account, *_ = account_sign_in

    assert account.status_code == 200
    assert 'token' in account.json()['data']

def test_sign_out(test_client, account_sign_in):
    account = test_client.patch(
        '/auth/sign-out/1/'
    )
    print(account.json()['data'])

    assert account.status_code == 200
    assert 'token' not in account.json()['data']
