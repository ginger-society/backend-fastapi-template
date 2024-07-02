from fastapi import APIRouter

from routes import predictor

router = APIRouter()
router.include_router(predictor.router, tags=["predictor"], prefix="/v1")
