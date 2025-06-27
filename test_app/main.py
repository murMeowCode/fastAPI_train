"""First fastAPI service"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Импортируем роутер.
from test_app.api.routers import main_router
from test_app.core.config import Settings
from test_app.core.init_db import create_first_superuser

@asynccontextmanager
async def lifespan(app: FastAPI): #pylint: disable=W0613
    """_summary_

    Args:
        app (FastAPI): _description_
    """
    # Startup code
    await create_first_superuser()
    yield

settings = Settings()

test_app = FastAPI(title=settings.app_title,lifespan=lifespan)

# Подключаем роутер.
test_app.include_router(main_router)
