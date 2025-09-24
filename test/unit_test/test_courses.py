import pytest, asyncio
from app.services.courses import course_service
from app.schemas.courses import CourseCreate, CourseUpdate
from app.services.errors import CourseExistError, CourseNotFoundError

fake_data = CourseCreate(
    title='Computer Science',
    instructor='Samson Ajifowoke',
    duration=4
)

@pytest.mark.asyncio
async def test_create_course(mock_courses_write, mock_courses_read, setup_course):
    course, courses = setup_course
    mock_courses_read.return_value = courses

    assert 'id' in course
    assert fake_data.title == course['title']

    with pytest.raises(CourseExistError) as exc:
        await course_service.create_course(fake_data)
    assert 'Course already exist!' == str(exc.value)

@pytest.mark.asyncio
async def test_get_courses(mock_courses_write, mock_courses_read, setup_course):
    course, courses = setup_course
    mock_courses_read.return_value = courses

    user_courses = await course_service.get_courses(fake_data.instructor)
    assert course in user_courses

    with pytest.raises(CourseNotFoundError) as exc:
        mock_courses_read.return_value = []
        await course_service.get_courses()
    assert 'Course not found!' == str(exc.value)

@pytest.mark.asyncio
async def test_get_course(mock_courses_write, mock_courses_read, setup_course):
    course, courses = setup_course
    mock_courses_read.return_value = courses

    user_course = await course_service.get_course(fake_data.title)
    assert course['title'] == user_course['title']

    with pytest.raises(CourseNotFoundError) as exc:
        await course_service.get_course('Biochemistry')
    assert 'Course not found!' == str(exc.value)

@pytest.mark.asyncio
async def test_update_course(mock_courses_write, mock_courses_read, setup_course):
    course, courses = setup_course
    mock_courses_read.return_value = courses

    fake_data1 = CourseUpdate(
        title='Medicine and surgery'
    )

    user_course = await course_service.update_course(course['id'], fake_data1)
    assert user_course['title'] == fake_data1.title

@pytest.mark.asyncio
async def test_delete_course(mock_courses_write, mock_courses_read, setup_course):
    course, courses = setup_course
    mock_courses_read.return_value = courses

    await course_service.delete_course(course['id'])

    assert course not in mock_courses_read.return_value
