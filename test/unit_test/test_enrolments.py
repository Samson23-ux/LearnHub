import pytest, asyncio
from app.schemas.enrolments import EnrolCreate
from app.services.enrolments import enrol_service
from app.services.errors import EnrolmentNotFoundError, EnrolmentExistError

fake_data = EnrolCreate(
        course_instructor='Samson Ajifowoke',
        course_title='Computer Science',
        student='Oluwatobiloba'
)

@pytest.mark.asyncio
async def test_create_enrolment(mock_enrol_write, mock_enrol_read, setup_enrolment):
    enrolment, enrolments = setup_enrolment
    mock_enrol_read.return_value = enrolments

    assert 'id' in enrolment
    assert enrolment['student'] == fake_data.student

    with pytest.raises(EnrolmentExistError) as exc:
        await enrol_service.create_enrolments(fake_data)
    assert 'User already enrolled!' == str(exc.value)

@pytest.mark.asyncio
async def test_get_enrolment(mock_enrol_write, mock_enrol_read, setup_enrolment):
    enrolment, enrolments = setup_enrolment
    mock_enrol_read.return_value = enrolments

    user_enrol = await enrol_service.get_enrolment_by_id(enrolment['id'], enrolments)

    assert enrolment['student'] == user_enrol['student']

    with pytest.raises(EnrolmentNotFoundError) as exc:
        enrolments = []
        await enrol_service.get_enrolment_by_id(enrolment['id'], enrolments)
    assert 'Enrolment not found!' == str(exc.value)

@pytest.mark.asyncio
async def test_get_enrolments(mock_enrol_write, mock_enrol_read, setup_enrolment):
    enrolment, enrolments = setup_enrolment
    mock_enrol_read.return_value = enrolments

    user_enrol = await enrol_service.get_enrolments(fake_data.course_instructor)

    assert enrolment in user_enrol

    with pytest.raises(EnrolmentNotFoundError) as exc:
        mock_enrol_read.return_value = []
        await enrol_service.get_enrolments(fake_data.course_instructor)
    assert 'Enrolment not found!' == str(exc.value)

@pytest.mark.asyncio
async def test_get_student_enrolments(mock_enrol_write, mock_enrol_read, setup_enrolment):
    enrolment, enrolments = setup_enrolment
    mock_enrol_read.return_value = enrolments

    user_enrol = await enrol_service.get_student_enrolments(fake_data.student)

    assert enrolment in user_enrol

    with pytest.raises(EnrolmentNotFoundError) as exc:
        mock_enrol_read.return_value = []
        await enrol_service.get_student_enrolments(fake_data.student)
    assert 'Enrolment not found!' == str(exc.value)

@pytest.mark.asyncio
async def test_delete_enrolment(mock_enrol_write, mock_enrol_read, setup_enrolment):
    enrolment, enrolments = setup_enrolment
    mock_enrol_read.return_value = enrolments

    await enrol_service.delete_enrolment(enrolment['id'])

    assert enrolment not in enrolments
