import pytest, asyncio
from app.schemas.users import AccountCreate
from app.services.admin import admin_service
from app.core.utils import hash_password

fake_data = AccountCreate(
        username='jojojojo',
        email='jojo@email.com',
        password='jojojojo123',
        role='Admin'
)

fake_data2 = AccountCreate(
        username='jojo gasmine',
        email='jojo@email.com',
        password='jojojojo123',
        role='Student'
)

@pytest.mark.asyncio
async def test_get_stats(
    mock_admin_write,
    mock_admin_read,
    setup_account,
    setup_course,
    setup_enrolment
):
    user, users = setup_account
    _, courses = setup_course
    enrol, enrolments = setup_enrolment

    user_stats = [users, courses, enrolments]
    mock_admin_read.return_value = user_stats

    stats = await admin_service.get_stats()

    assert 'users' in stats
    assert 'courses' in stats
    assert 'enrolments' in stats

@pytest.mark.asyncio
async def test_delete_account(mock_admin_write, mock_admin_read, setup_account):
    user, users = setup_account
    mock_admin_read.return_value = users

    user_acc = fake_data.model_dump()
    user_acc['password'] = hash_password(user_acc['password'])

    await admin_service.delete_account(user_acc, '2',
                                       fake_data.password)

    assert user not in users
