from fastapi import APIRouter
import random

router = APIRouter(tags=["Fines"])


@router.get("/fines/{user_id}")
async def check_fines(user_id: int):
    has_fines = False
    
    if has_fines:
        return {
            "user_id": user_id,
            "has_fines": True,
            "message": "У вас есть штрафы",
            "fines_count": random.randint(1, 3),
            "total_amount": random.randint(1, 10000)
        }
    else:
        return {
            "user_id": user_id,
            "has_fines": False,
            "message": "У вас нет штрафов",
            "fines_count": 0
        }