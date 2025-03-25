from fastapi import APIRouter
from src.schemas.user_schema import UserResponse
from src.models.user import User


router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate)