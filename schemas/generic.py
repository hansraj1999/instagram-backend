from pydantic import BaseModel, Field
from typing import List, Dict


class ErrorResponse(BaseModel):
    # {
    #   "status": "error",
    #   "message": "Invalid request. 'caption' field is required.",
    #   "errors": [
    #     {
    #       "field": "caption",
    #       "message": "Caption cannot be empty."
    #     }
    #   ]
    # }
    status: str
    message: str | None = None
    errors: List[Dict[str, str]]


class XUserData(BaseModel):
    user_id: int
    role: str
    user_name: str


class SucessResponse(BaseModel):
    status: str
    message: str
