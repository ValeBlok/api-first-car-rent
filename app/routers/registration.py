import logging

from fastapi import APIRouter, status

from app import storage
from app.models import UserCreate, UserCreated

router = APIRouter(tags=["Users"])
logger = logging.getLogger("car_rent.registration")


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
    logger.info(
        "user_registered",
        extra={
            "user_id": user_id,
            "license_number": user.license_number,
            "age": user.age,
        },
    )

    return UserCreated(user_id=user_id, message="Регистрация успешна")
