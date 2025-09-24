from fastapi import APIRouter, Depends, Query, Form
from app.services.admin import admin_service
from app.dependencies import required_role
from app.schemas.users import Response

router = APIRouter()

@router.get('/stats/', response_model=Response)
async def get_stats(
    users: str = Query(None, description='Filter by users'),
    courses: str = Query(None, description='Filter by courses'),
    enrolments: str = Query(None, description='Filter by courses'),
    _ = Depends(required_role('admin'))
):
    stats = await admin_service.get_stats(users, courses, enrolments)

    return Response(message='Stats retrieved successfully!', data=stats)

@router.delete('/users/{acc_id}/', status_code=204)
async def delete_account(
    acc_id: str,
    password: str = Form(...),
    user: dict = Depends(required_role('admin'))
):
    await admin_service.delete_account(user, acc_id, password)

    return Response(message='Account deleted successfully!')
