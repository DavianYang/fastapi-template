from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from app.config import get_settings, Settings
from app.events.app_handlers import create_start_app_handler, create_stop_app_handler
from app.api.routes.api import router as api_router

def get_application(settings: Settings = get_settings()) -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION
    )
    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))
    
    application.include_router(api_router, prefix=settings.API_PREFIX)
    
    return application

app = get_application()