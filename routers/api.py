from typing import List

from fastapi import APIRouter
from models import Exchanger, Exchanger_Pydantic

router = APIRouter(
    tags=['API Exchanger']
)


@router.get('/courses', response_model=Exchanger_Pydantic)
async def get_courses():
    pass
