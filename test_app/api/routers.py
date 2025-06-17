from fastapi import APIRouter

from test_app.api.endpoints.meeting_room import router as room_router
from test_app.api.endpoints.reservation import router as reservation_router

main_router = APIRouter()
main_router.include_router(room_router)
main_router.include_router(reservation_router)
