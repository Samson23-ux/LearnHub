from fastapi import APIRouter, Query, Depends
from app.schemas.courses import CourseCreate, CourseUpdate, Response
from app.services.courses import course_service
from app.dependencies import get_current_user, required_role

router = APIRouter()

@router.get('/', response_model=Response)
async def get_courses(
    instructor: str = Query(None, description='Filter by instructor'),
    _ = Depends(get_current_user)
):
    courses = await course_service.get_courses(instructor)

    return Response(message='Courses retrieved successfully!', data=courses)

@router.get('/{title}/', response_model=Response)
async def get_course(title: str, _ = Depends(get_current_user)):
    course = await course_service.get_course(title)

    return Response(message='Course retrieved successfully!', data=course)

@router.post('/', status_code=201, response_model=Response)
async def create_course(
    course_create: CourseCreate,
    instructor: dict = Depends(required_role('Instructor'))
):
    course = await course_service.create_course(course_create)

    return Response(message='Course created successfully!', data=course)

@router.patch('/{course_id}/', response_model=Response)
async def update_course(
    course_id: str,
    course_update: CourseUpdate,
    instructor: dict = Depends(required_role('Instructor'))
):
    course = await course_service.update_course(course_id, course_update)

    return Response(message='Course updated successfully!', data=course)

@router.delete('/{course_id}/', status_code=204)
async def delete_course(
    course_id: str,
    instructor: dict = Depends(required_role('Instructor'))
):
    await course_service.delete_course(course_id)

    return Response(message='Course deleted successfully!')
