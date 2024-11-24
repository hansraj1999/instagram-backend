from fastapi import APIRouter, HTTPException
import logging
from fastapi import Header
import traceback
from pydantic import ValidationError
from posts.schemas import CreatePostRequest
from posts.foreground.create import create_post
from auth import validate_headers

logger = logging.getLogger(__name__)
router = APIRouter(tags=["post"], prefix="/post")


# On the Server Side:
# The server is typically responsible for interfacing with the client, performing application-specific logic, and publishing events to Kafka when specific actions occur. Here’s a breakdown of tasks on the server:

# Post Creation:

# Validate incoming post data (e.g., text, images, tags).
# Create the post entry in the database (e.g., MySQL).
# Publish an event to the Kafka topic post-creation-events with all post-related data (post content, user ID, timestamp, etc.).
# Post Update:

# Validate and process the updated data (e.g., changed caption, tags).
# Update the post record in the database.
# Publish an event to the Kafka topic post-update-events containing the updated data (post ID, new content, etc.).
# Post Engagement (Likes and Comments):

# When a user likes a post or adds a comment, update the post's metadata in the database (e.g., increment the like count or add a comment to the list).
# Publish a message to the relevant Kafka topic (post-like-events or post-comment-events) with necessary data (e.g., post ID, user ID, comment text, timestamp).
# Post Deletion:

# Delete the post entry from the database.
# Publish an event to the Kafka topic post-deletion-events to notify other parts of the system about the deletion.
# Media Processing:

# Handle any media processing tasks (e.g., generating thumbnails for images, processing video files).
# Publish events to the post-media-processing-events topic when processing is complete or when further actions are needed


@router.post("/", response_model=CreatePostRequest)
async def shorten_url_endpoint(request: CreatePostRequest, headers: str = Header(...)):
    try:
        headers = validate_headers(headers)
        resposne = create_post(request, headers)
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
