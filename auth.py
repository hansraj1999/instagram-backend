from typing import Dict
import ujson
from pydantic import ValidationError
import logging
from pydantic import ValidationError
from schemas.generic import XUserData

logger = logging.getLogger(__name__)


def validate_headers(headers: str) -> XUserData:
    try:
        headers_dict = ujson.loads(headers)  # TODO: Use orjson it is faster
        XUserData(**headers_dict)
    except ValidationError as e:
        raise e
    return headers_dict
