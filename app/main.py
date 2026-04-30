from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator
import os

from app.api.routes import router

app = FastAPI(
    title="SentryOps",
    description="DevSecOps Infrastructure Monitoring Platform",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")

Instrumentator().instrument(app).expose(app)

static_dir = os.path.join(os.path.dirname(__file__), "static")


@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join(static_dir, "index.html"), "r") as f:
        return f.read()
