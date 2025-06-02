"""First fastAPI service"""
from fastapi import FastAPI

# Импортируем роутер.
from test_app.api.meeting_room import router
from test_app.core.config import Settings

settings = Settings()

test_app = FastAPI(title=settings.app_title)

# Подключаем роутер.
test_app.include_router(router)
