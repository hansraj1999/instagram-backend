from posts.foreground.create import create_post

CONSUMER_TYPE_TO_TOPICS = {
    "POST_PROCESSOR": [
        "post-creation-events",
        "post-update-events",
        "post-media-processing-events",
    ]
}

EVENTS_TO_TAKS = {"create_post": {"task": create_post}}
