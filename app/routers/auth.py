from fastapi import APIRouter
from app.schemas.users import AccountCreate, AccountSignIn, Response
from app.services.users import account_service

router = APIRouter()

@router.post('/sign-up/', status_code=201, response_model=Response)
async def sign_up(account_create: AccountCreate):
    account = await account_service.create_account(account_create)

    return Response(message='Account created successfully!', data=account)

@router.post('/sign-in/{acc_id}/', response_model=Response)
async def sign_in(acc_id: str, account_create: AccountSignIn):
    account = await account_service.sign_in(acc_id, account_create)

    return Response(message='Sign-in successfully!', data=account)

@router.patch('/sign-out/{acc_id}/', response_model=Response)
async def sign_out(acc_id: str):
    account = await account_service.sign_out(acc_id)

    return Response(message='Sign-out successfully!', data=account)
