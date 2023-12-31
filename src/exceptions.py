from starlette.responses import JSONResponse

from src.schemes import ApiResponse


class GeneralException(Exception):
    def __init__(self, status_code: int, message: str, error_code: int, error_message: str):
        self.status_code = status_code
        self.message = message
        self.error_code = error_code
        self.error_message = error_message

    def as_response(self):
        response = ApiResponse(
            status_code=self.status_code,
            success=False,
            message=self.message,
            error_code=self.error_code,
            error_message=self.error_message,
            data=None
        )
        return JSONResponse(response.as_dict())
