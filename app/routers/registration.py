from fastapi import APIRouter, status

from app import storage
from app.models import UserCreate, UserCreated

router = APIRouter(tags=["Users"])


@router.post(
    "/registration",
    operation_id="registerUser",
    response_model=UserCreated,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(user: UserCreate) -> UserCreated:
    user_id = storage.next_user_id
    storage.next_user_id += 1
    storage.users[user_id] = user.model_dump()

    return UserCreated(user_id=user_id, message="Регистрация успешна")
