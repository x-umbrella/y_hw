from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from src.api.v1.schemas import PostCreate, PostListResponse, PostModel
from src.services import PostService, get_post_service
from src.services import UserService, get_user_service


router = APIRouter()


@router.get(
    path="/",
    response_model=PostListResponse,
    summary="Список постов",
    tags=["posts"],
)
def post_list(
    post_service: PostService = Depends(get_post_service),
) -> PostListResponse:
    posts: dict = post_service.get_post_list()
    if not posts:
        # Если посты не найдены, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="posts not found")
    return PostListResponse(**posts)


@router.get(
    path="/{post_id}",
    response_model=PostModel,
    summary="Получить определенный пост",
    tags=["posts"],
)
def post_detail(
    post_id: int, post_service: PostService = Depends(get_post_service)
) -> PostModel:
    print(f"post_id: {post_id}")
    post: Optional[dict] = post_service.get_post_detail(item_id=post_id)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="post not found")
    return PostModel(**post)


@router.post(
    path='/',
    response_model=PostModel,
    summary='Создать пост',
    tags=['posts'],
    status_code=status.HTTP_201_CREATED,
)
def post_create(
    post: PostCreate,
    auth: AuthJWT = Depends(),
    post_service: PostService = Depends(get_post_service),
    user_service: UserService = Depends(get_user_service)
) -> PostModel:
    if user_service.get_user_by_access_token(auth):
        post: dict = post_service.create_post(post=post)
        return PostModel(**post)
    else:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='User not authorized')

