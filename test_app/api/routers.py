"""module for main router creating combining less hierarchichal routers"""
from fastapi import APIRouter

from test_app.api.endpoints import room_router, reservation_router

main_router = APIRouter()
main_router.include_router(
    room_router, prefix='/meeting_rooms', tags=['Meeting Rooms']
)
main_router.include_router(
    reservation_router, prefix='/reservations', tags=['Reservations']
)
