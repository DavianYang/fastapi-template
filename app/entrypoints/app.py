from fastapi import FastAPI, applications
from starlette.middleware.cors import CORSMiddleware

from app.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.router.api import router as api_router

def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    
    application.add_middleware(
     CORSMiddleware,
     allow_origins=ALLOWED_HOSTS or ["*"],
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"]
    )
    
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))
    
    application.include_router(api_router, prefix=API_PREFIX)
    
    return application

app = get_application()
    
    