from fastapi import APIRouter, HTTPException
import logging
from fastapi import Header
import traceback
from pydantic import ValidationError

logger = logging.getLogger(__name__)
router = APIRouter(tags=["short-url"], prefix="/v1")


@router.post("/shorten", response_model=ShortenUrlResponse)
async def shorten_url_endpoint(
    request: ShortenTheURLRequestBody, headers: str = Header(...)
):
    try:
        # {"x-user-data": { "user_id": 1, "role": "admin", "user_name": "admin" }}
        headers = validate_headers(headers)
        user_data = headers["x-user-data"]
        handler = Handler(request.long_url, request.group_guid, user_data)
        short_url = handler.handle()
        return {"short_url": short_url}


    except ValidationError as e:
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Validation Error",
                "details": e.errors(include_url=False, include_input=False),
            },
        )
    except Exception as e:
        traceback.print_exc()
        logger.exception(str(e))
        raise HTTPException(status_code=400, detail={"message": str(e), "details": []})