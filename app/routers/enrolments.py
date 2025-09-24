from fastapi import APIRouter, Depends
from app.services.enrolments import enrol_service
from app.schemas.enrolments import EnrolCreate, Response
from app.dependencies import required_role

router = APIRouter()

@router.get('/enrolments/{student}/', response_model=Response)
async def get_student_enrolments(
    student: str,
    _ = Depends(required_role('student'))
):
    enrolments = await enrol_service.get_student_enrolments(student)

    return Response(message='Enrolments retrieved successfully!', data=enrolments)

@router.get('/{instructor}/enrolments/', response_model=Response)
async def get_enrolments(
    instructor: str,
    _ = Depends(required_role('instructor'))
):
    enrolments = await enrol_service.get_enrolments(instructor)

    return Response(message='Course enrolments retrieved successfully!',
                    data=enrolments)

@router.post('/enrolments/', status_code=201, response_model=Response)
async def create_enrolment(
    enrol_create: EnrolCreate,
    _ = Depends(required_role('student'))
):
    enrolment = await enrol_service.create_enrolments(enrol_create)

    return Response(message='Course enrolled successfully!', data=enrolment)

@router.delete('/enrolments/{enrol_id}/', status_code=204)
async def delete_enrolments(enrol_id: str, _ = Depends(required_role('student'))):
    await enrol_service.delete_enrolment(enrol_id)

    return Response(message='Enrolment canceled successfully!')
