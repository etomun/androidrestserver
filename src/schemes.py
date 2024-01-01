from datetime import datetime
from typing import Optional, TypeVar, Generic

from pydantic import BaseModel

from src.utils import date_time_to_str_gmt

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    status_code: int = 200
    success: bool = True
    message: str = "Success"
    error_code: int = 0
    error_message: str = ""
    data: Optional[T] = None

    def as_dict(self) -> dict:
        return {
            "status_code": self.status_code,
            "success": self.success,
            "message": self.message,
            "content": {
                "error_code": self.error_code,
                "error_message": self.error_message,
                "data": self._convert_datetime(self.data)
            }
        }

    def _convert_datetime(self, value):
        if isinstance(value, datetime):
            return date_time_to_str_gmt(value)
        elif isinstance(value, list):
            return [self._convert_datetime(item) for item in value]
        elif isinstance(value, dict):
            return {key: self._convert_datetime(item) for key, item in value.items()}
        else:
            return value
