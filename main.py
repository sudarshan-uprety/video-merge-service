import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.merge_video.router import router as merge_router


logging.basicConfig(level=logging.INFO)


app = FastAPI(
    title="Video service.",
    description="This is a service which is responsible for merging multiple videos.",
    docs_url="/api/docs/",
)


def register_middlewares(server):
    # Initialize CORS
    server.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )


def register_routes(server):
    server.include_router(merge_router)


register_routes(server=app)
register_middlewares(server=app)

