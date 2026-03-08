from fastapi import APIRouter
from models import UserCreation
import random

router = APIRouter(tags=["Users"])

@router.post("/registration")
async def register_user(user: UserCreation):
    return {
        "user_id": random.randint(1, 100),
        "message": "Регистрация успешна"
    }