"""base for alembic.env"""
#pylint: disable=W0611
from test_app.core.db import Base #noqa
from test_app.models.meeting_room import MeetingRoom  #noqa
from test_app.models.reservation import Reservation #noqa
