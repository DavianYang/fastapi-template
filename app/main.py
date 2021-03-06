from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.api import router as api_router
from app.config import Settings, settings
from app.events.app_handlers import create_start_app_handler, create_stop_app_handler


def get_application(settings: Settings = settings) -> FastAPI:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOWED_HOSTS or ["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ]

    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        middleware=middleware,
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(api_router, prefix=settings.API_PREFIX)

    return application


app = get_application()
