from fastapi import APIRouter, status

from app import storage
from app.models import FineCreate, FineCreated, UserFines

router = APIRouter(tags=["Fines"])


@router.get(
    "/fines/{user_id}",
    operation_id="getUserFines",
    response_model=UserFines,
)
async def get_user_fines(user_id: int) -> UserFines:
    user_fines = storage.fines.get(user_id, [])
    total_amount = sum(fine["amount"] for fine in user_fines)
    has_fines = len(user_fines) > 0

    return UserFines(
        user_id=user_id,
        has_fines=has_fines,
        fines_count=len(user_fines),
        total_amount=total_amount,
        message="У пользователя есть штрафы" if has_fines else "У пользователя нет штрафов",
    )


@router.post(
    "/fines",
    operation_id="createFine",
    response_model=FineCreated,
    status_code=status.HTTP_201_CREATED,
)
async def create_fine(fine: FineCreate) -> FineCreated:
    fine_id = storage.next_fine_id
    storage.next_fine_id += 1

    created_fine = FineCreated(
        fine_id=fine_id,
        user_id=fine.user_id,
        amount=fine.amount,
        reason=fine.reason,
        status="created",
    )
    storage.fines.setdefault(fine.user_id, []).append(created_fine.model_dump())

    return created_fine
