from datetime import datetime
from typing import Optional, TypeVar, Generic

from pydantic import BaseModel
from pydantic.v1 import validator

from src.utils import convert_datetime_to_gmt

T = TypeVar("T")


class ApiRequest(BaseModel):
    @validator("*", pre=True, always=True)
    def validate_date_format(self, value, field):
        if field.name == "date" and isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                raise ValueError("Invalid date format. Use '%Y-%m-%dT%H:%M:%S' in UTC.")
        return value


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
            return convert_datetime_to_gmt(value)
        elif isinstance(value, list):
            return [self._convert_datetime(item) for item in value]
        elif isinstance(value, dict):
            return {key: self._convert_datetime(item) for key, item in value.items()}
        else:
            return value
