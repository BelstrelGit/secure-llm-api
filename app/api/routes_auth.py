from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.core.errors import ConflictError, NotFoundError, UnauthorizedError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    body: RegisterRequest,
    usecase: Annotated[AuthUseCase, Depends(get_auth_usecase)],
):
    try:
        user = await usecase.register(email=body.email, password=body.password)
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    usecase: Annotated[AuthUseCase, Depends(get_auth_usecase)],
):
    try:
        token = await usecase.login(email=form.username, password=form.password)
    except UnauthorizedError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exc.detail)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserPublic)
async def me(
    user_id: Annotated[int, Depends(get_current_user_id)],
    usecase: Annotated[AuthUseCase, Depends(get_auth_usecase)],
):
    try:
        user = await usecase.get_profile(user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.detail)
    return user
