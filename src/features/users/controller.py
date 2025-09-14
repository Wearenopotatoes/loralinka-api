from typing import List

from fastapi import APIRouter, HTTPException, status
from src.database.db import DbSession

from .model import UserCreate, UserUpdate, UserOut, LoginRequest
from . import service

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def create_user(db: DbSession, payload: UserCreate) -> UserOut:
    user = service.create_user(db, payload)
    return UserOut.model_validate(user)


@router.post(
    "/login",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
)
def login(payload: LoginRequest, db: DbSession) -> UserOut:
    user = service.authenticate_user(db, payload.phone, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return UserOut.model_validate(user)


@router.get(
    "",
    response_model=List[UserOut],
)
def list_users(db: DbSession, skip: int = 0, limit: int = 100) -> List[UserOut]:
    users = service.list_users(db, skip=skip, limit=limit)
    return [UserOut.model_validate(u) for u in users]


@router.get(
    "/{user_id}",
    response_model=UserOut,
)
def get_user(user_id: int, db: DbSession) -> UserOut:
    user = service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut.model_validate(user)


@router.put(
    "/{user_id}",
    response_model=UserOut,
)
def update_user(user_id: int, payload: UserUpdate, db: DbSession) -> UserOut:
    user = service.update_user(db, user_id, payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut.model_validate(user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(user_id: int, db: DbSession) -> None:
    ok = service.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return None