from typing import Dict
import ujson
from pydantic import ValidationError
import logging
from pydantic import ValidationError
from schemas.generic import UserData

logger = logging.getLogger(__name__)


def validate_headers(headers: str) -> UserData:
    try:
        headers_dict = ujson.loads(headers)
        UserData(**headers_dict)
    except ValidationError as e:
        raise e
    return headers_dict
