import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
import logging
import socket

from routers.post import post_router

logger = logging.getLogger(__name__)


def start_server():
    app = FastAPI()

    FastAPIInstrumentor.instrument_app(app)
    RedisInstrumentor().instrument()
    PymongoInstrumentor().instrument()
    RequestsInstrumentor().instrument()
    AioHttpClientInstrumentor().instrument()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(post_router)

    @app.get("/")
    async def read_item():
        logger.info(socket.gethostname())
        return {"home_page": f"hello {socket.gethostname()}"}

    @app.get("/healthz")
    async def healthz():
        logger.info(f"health check done, {socket.gethostname()}")
        return {"ping": f"health check done {socket.gethostname()}"}

    @app.get("/metrics")
    async def metrics():
        logger.info("metrics endpoint called")

    return app
