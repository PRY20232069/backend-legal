from fastapi import APIRouter

router = APIRouter(
    prefix='/api/v2/feedback',
    tags=['Feedback'],
)