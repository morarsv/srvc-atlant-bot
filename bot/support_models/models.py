import logging
from typing import TypedDict
from uuid import UUID
from datetime import datetime


class SupportSessionUser(TypedDict):
    username: str
    login: str
    role_id: int
    user_uuid: UUID
    company_id: int
    company_name: str


class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='{', tz=None):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.tz = tz

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, tz=self.tz)
        if datefmt:
            return dt.strftime(datefmt)
        else:
            return dt.isoformat()
