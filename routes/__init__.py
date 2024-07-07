from fastapi import APIRouter

from routes import predictor

router = APIRouter()
router.include_router(predictor.router, prefix="/v1")
