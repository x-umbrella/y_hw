from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from src.api.v1.schemas import UserEmail
from src.services import UserService, get_user_service


router = APIRouter()


@router.get(
    path='/',
    summary='Данные пользователя',
    tags=['users_me'],
)
def user_info(
    user_service: UserService = Depends(get_user_service),
    auth: AuthJWT = Depends(),
):
    return user_service.user_info(auth)


@router.patch(
    path='/',
    summary='Изменить пользовательские данные',
    tags=['users_me'],
)
def user_modify(
    user: UserEmail,
    user_service: UserService = Depends(get_user_service),
    auth: AuthJWT = Depends(),
):
    return user_service.user_modify(auth, user=user)