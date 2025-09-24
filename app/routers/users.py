from fastapi import APIRouter, Query, Depends
from app.schemas.users import AccountUpdate, PasswordUpdate, Response
from app.services.users import account_service
from app.dependencies import get_current_user

router = APIRouter()

@router.get('/', response_model=Response)
async def get_users(
    role: str = Query(None, description='Filter by role'),
    _ = Depends(get_current_user)
):
    users = await account_service.get_accounts(role)

    return Response(message='Users retrieved successfully', data=users)

@router.get('/{username}/', response_model=Response)
async def get_user(username: str, _ = Depends(get_current_user)):
    user = await account_service.get_account(username)

    return Response(message='User retrieved', data=user)

@router.patch('/{acc_id}/', response_model=Response)
async def update_user_details(
    acc_id: str,
    acc_update: AccountUpdate,
    _ = Depends(get_current_user)
):
    user = await account_service.update_account(acc_id, acc_update)

    return Response(message='Account updated successfully', data=user)

@router.patch('/{acc_id}/update-password/', response_model=Response)
async def update_password(
    acc_id: str,
    password_update: PasswordUpdate,
    _ = Depends(get_current_user)
):
    user = await account_service.update_password(acc_id, password_update)

    return Response(message='Password updated successfully', data=user)
