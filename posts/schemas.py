from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from enum import Enum
from schemas.generic import SucessResponse


class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"


class Media(BaseModel):
    type: MediaType  # Type of media (e.g., 'image', 'video')
    url: HttpUrl  # URL of the media file
    thumbnail_url: HttpUrl  # Thumbnail URL of the media
    order: int  # Order of the media item


class LocationMetadata(BaseModel):
    latitude: float  # Latitude of the location
    longitude: float  # Longitude of the location


class Preferences(BaseModel):
    enable_comments: bool  # Whether comments are enabled
    enable_sharing: bool  # Whether sharing is enabled


class CreatePostRequest(BaseModel):
    # {
    #   "user_id": 123,                          // ID of the user creating the post
    #   "caption": "Check out this amazing sunset!",  // The caption text for the post
    #   "tags": ["sunset", "nature", "photography"], // Array of tags associated with the post
    #   "location": "California, USA",              // The location where the post was taken
    #   "media": [                                 // Array of media objects (image, video, etc.)
    #     {
    #       "type": "image",                        // Type of media (image, video)
    #       "url": "https://cdn.example.com/image1.jpg",  // URL of the media file (can be CDN URL)
    #       "thumbnail_url": "https://cdn.example.com/thumb_image1.jpg", // URL for the media thumbnail
    #       "order": 1                               // Order of media if multiple files are included
    #     },
    #     {
    #       "type": "video",                        // Another media type (video)
    #       "url": "https://cdn.example.com/video1.mp4",  // URL of the media file (video)
    #       "thumbnail_url": "https://cdn.example.com/thumb_video1.jpg", // Thumbnail for the video
    #       "order": 2                               // Order of media
    #     }
    #   ],
    #   "is_private": false,                      // Whether the post is private (default: false)
    #   "is_verified": false,                     // Whether the post is verified (default: false)
    #   "preferences": {                          // Any additional preferences or settings
    #     "enable_comments": true,                // Allow or block comments on the post
    #     "enable_sharing": true                  // Allow or block sharing of the post
    #   },
    #   "location_metadata": {                    // Optional: location-based data for the post
    #     "latitude": 37.7749,
    #     "longitude": -122.4194
    #   }
    # }
    user_id: int
    caption: Optional[str]
    tags: List[str]
    location: Optional[str] = "location"
    media: List[Media]
    is_private: bool = False
    is_verified: bool = False
    preferences: Preferences
    location_metadata: Optional[LocationMetadata] = None


class CreatePostResponse(SucessResponse):
    post_id: int
