from fastapi import APIRouter, HTTPException
import logging
from fastapi import Header
import traceback
from pydantic import ValidationError
from posts.schemas import CreatePostRequest, CreatePostResponse
from posts.foreground import create
from auth import validate_headers

logger = logging.getLogger(__name__)
post_router = APIRouter(tags=["post"], prefix="/post")


@post_router.post("/", response_model=CreatePostResponse)
async def create_post(request: CreatePostRequest, x_user_data: str = Header(...)):
    try:
        headers = validate_headers(x_user_data)
        resposne = await create.create_post(request, headers)
        return resposne
    except ValidationError as e:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "error",
                "message": "Validation Error",
                "errors": e.errors(include_url=False, include_input=False),
            },
        )
    except Exception as e:
        traceback.print_exc()
        logger.exception(str(e))
        raise HTTPException(
            status_code=400, detail={"status": "error", "message": str(e), "errors": []}
        )
