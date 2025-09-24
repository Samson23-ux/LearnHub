import pytest, asyncio
from app.services.users import account_service
from app.schemas.users import AccountCreate, AccountUpdate
from app.schemas.users import PasswordUpdate, AccountSignIn
from app.services.errors import UserNotFoundError, UserExistError
from app.services.errors import PasswordError, EmailError
from app.core.utils import hash_password


fake_data = AccountCreate(
        username='jojojojo',
        email='jojo@email.com',
        password='jojojojo123',
        role='Admin'
)

fake_data2 = AccountCreate(
        username='jojorabbit',
        email='jojo123@email.com',
        password='jojojojo123',
        role='Instructor'
)

fake_data3 = AccountUpdate(
    email='jojorabb123@email.com',
    curr_password='jojojojo123'
)

fake_data4 = AccountSignIn(
    email=fake_data.email,
    password=fake_data.password
)

fake_data5 = AccountSignIn(
    email='dada@email.com',
    password=fake_data.password
)

fake_data6 = AccountSignIn(
    email=fake_data.email,
    password='fake_data.password'
)

@pytest.mark.asyncio
async def test_create_account(mock_users_read, mock_users_write, setup_account):
    user, users = setup_account
    mock_users_read.return_value = users

    assert 'role' in user
    assert 'id' in user

    with pytest.raises(UserExistError):
        await account_service.create_account(fake_data)

    mock_users_write.assert_called_with('users.json', users)

@pytest.mark.asyncio
async def test_sign_in(mock_users_read, mock_users_write, setup_account):
    user, users = setup_account
    mock_users_read.return_value = users

    user_acc = await account_service.sign_in(user['id'], fake_data4)

    assert 'token' in user_acc

    with pytest.raises(EmailError) as exc:
        await account_service.sign_in(user['id'], fake_data5)
    assert 'Invalid email!' == str(exc.value)

    with pytest.raises(PasswordError) as exc:
        await account_service.sign_in(user['id'], fake_data6)
    assert 'Incorrect Password!' == str(exc.value)

@pytest.mark.asyncio
async def test_sign_out(mock_users_read, mock_users_write, setup_account):
    user, users = setup_account
    mock_users_read.return_value = users

    await account_service.sign_in(user['id'], fake_data4)
    await account_service.sign_out(user['id'])
    user_acc = await account_service.get_account(fake_data.username)

    assert 'token' not in user_acc

@pytest.mark.asyncio
async def test_get_account(mock_users_read, setup_account):
    _, users = setup_account
    mock_users_read.return_value = users

    account = await account_service.get_account(fake_data.username)

    assert account['username'] == 'jojojojo'
    assert account['email'] == 'jojo@email.com'

    with pytest.raises(UserNotFoundError):
        await account_service.get_account(fake_data2.username)

@pytest.mark.asyncio
async def test_get_accounts(mock_users_read, mock_users_write, setup_account):
    _, users = setup_account
    mock_users_read.return_value = users
    await account_service.create_account(fake_data2)

    accounts = await account_service.get_accounts()

    assert len(accounts) >= 1

@pytest.mark.asyncio
async def test_update_account(mock_users_read, mock_users_write, setup_account):
    user, users = setup_account
    mock_users_read.return_value = users

    account = await account_service.update_account(user['id'], fake_data3)

    assert account['email'] == fake_data3.email

    mock_users_write.assert_called_with('users.json', users)

@pytest.mark.asyncio
async def test_update_password(mock_users_read, mock_users_write, setup_account):
    user, users = setup_account
    mock_users_read.return_value = users

    password_update = PasswordUpdate(
        curr_password=fake_data.password,
        new_password='jojorabbit55'
    )

    await account_service.update_password(user['id'], password_update)
    account = account_service.get_acc_by_id('1', users)

    assert account['password'] == hash_password('jojorabbit55')

    mock_users_write.assert_called_with('users.json', users)
