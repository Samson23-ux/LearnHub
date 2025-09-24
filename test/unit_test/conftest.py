import pytest, asyncio
import pytest_asyncio
from unittest.mock import patch
from app.schemas.users import AccountCreate
from app.schemas.courses import CourseCreate
from app.schemas.enrolments import EnrolCreate
from app.services.users import account_service
from app.services.courses import course_service
from app.services.enrolments import enrol_service

@pytest.fixture
def mock_users_write():
    with patch('app.services.users.write_json') as mock_write:
        yield mock_write

@pytest.fixture
def mock_users_read():
    with patch('app.services.users.read_json') as mock_read:
        yield mock_read

@pytest.fixture
def mock_admin_write():
    with patch('app.services.admin.write_json') as mock_write:
        yield mock_write

@pytest.fixture
def mock_admin_read():
    with patch('app.services.admin.read_json') as mock_read:
        yield mock_read

@pytest.fixture
def mock_courses_write():
    with patch('app.services.courses.write_json') as mock_write:
        yield mock_write

@pytest.fixture
def mock_courses_read():
    with patch('app.services.courses.read_json') as mock_read:
        yield mock_read

@pytest.fixture
def mock_enrol_write():
    with patch('app.services.enrolments.write_json') as mock_write:
        yield mock_write

@pytest.fixture
def mock_enrol_read():
    with patch('app.services.enrolments.read_json') as mock_read:
        yield mock_read

@pytest_asyncio.fixture
async def setup_account(mock_users_write, mock_users_read):
    fake_data = AccountCreate(
        username='jojojojo',
        email='jojo@email.com',
        password='jojojojo123',
        role='Admin'
    )

    fake_data2 = AccountCreate(
        username='jojo gasmine',
        email='jojogg@email.com',
        password='jojojojo123',
        role='Student'
    )

    mock_users_read.return_value = []
    user = await account_service.create_account(fake_data)
    await account_service.create_account(fake_data2)
    return user, mock_users_read.return_value

@pytest_asyncio.fixture
async def setup_course(mock_courses_write, mock_courses_read):
    fake_data = CourseCreate(
        title='Computer Science',
        instructor='Samson Ajifowoke',
        duration=4
    )

    mock_courses_read.return_value = []
    course = await course_service.create_course(fake_data)

    mock_courses_write.assert_called_with('courses.json', mock_courses_read.return_value)
    return course, mock_courses_read.return_value

@pytest_asyncio.fixture
async def setup_enrolment(mock_enrol_write, mock_enrol_read):
    fake_data = EnrolCreate(
        course_instructor='Samson Ajifowoke',
        course_title='Computer Science',
        student='Oluwatobiloba'
    )

    mock_enrol_read.return_value = []
    enrolment = await enrol_service.create_enrolments(fake_data)

    mock_enrol_write.assert_called_with('enrolments.json', mock_enrol_read.return_value)
    return enrolment, mock_enrol_read.return_value
