from fastapi import FastAPI, Request
import time
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import router as api_router
from settings import settings
from lifetime import register_shutdown_event, register_startup_event
from http import HTTPStatus
from prometheus_fastapi_instrumentator import Instrumentator
from core.monitoring import http_requested_languages_total


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        servers=[
            {"url": "https://api.example.com", "description": "Production server"},
        ],
    )
    application.include_router(api_router, prefix=settings.API_PREFIX)
    pre_load = False
    register_startup_event(application)
    register_shutdown_event(application)
    instrumentator = Instrumentator()
    instrumentator.add(http_requested_languages_total())
    instrumentator.instrument(application).expose(application)

    @application.middleware("http")
    # type: ignore
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allows all headers
    )

    return application


app = get_application()
