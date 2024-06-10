from fastapi import APIRouter, HTTPException, status
import services.user_services
from common.authorization import create_token, get_current_user
from security.password_hashing import get_password_hash, verify_password
from services import user_services
from data.schemas import UserCreate, UserLogin, UpdateAmount, UpdateProfile
from fastapi import Depends

users_router = APIRouter(prefix='/users')


@users_router.get('/balance')
def get_account_balance(user_id: int = Depends(get_current_user)):
    balance = user_services.get_account_balance(user_id)
    return balance


@users_router.post('/register', status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate):
    new_user = user_services.create(user_create.username, user_create.password, user_create.email,
                                    user_create.phone_number)
    return new_user


@users_router.post('/login', status_code=status.HTTP_200_OK)
def login(user_login: UserLogin):
    user = user_services.try_login(user_login.email, user_login.password)

    access_token = create_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@users_router.put('/profile/update')
def update_profile(update_profile_params: UpdateProfile, user: int = Depends(get_current_user)):
    result = user_services.update_profile(update_profile_params.password, update_profile_params.email,
                                          update_profile_params.phone_number, user)
    return result


@users_router.get('/profile')
def get_logged_user(user: int = Depends(get_current_user)):
    result = user_services.get_logged_user(user)
    return result
