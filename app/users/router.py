from fastapi import Response, APIRouter
from fastapi.params import Depends
from app.users.auth import *
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SAuthUser
from app.exeptions import *
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
router2 = APIRouter(
    prefix="/auth",
    tags=["Пользователи"]
)
@router.post("/register")
async def register_user(user_data: SAuthUser):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login_user(response: Response, user_data: SAuthUser):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub":str(user.id)})
    response.set_cookie("booking_access_token", access_token,httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")

@router2.post("/me")
async def read_user_me(current_user: Users = Depends(get_current_user)):
    return current_user
