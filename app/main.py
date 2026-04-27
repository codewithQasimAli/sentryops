from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes import router

app = FastAPI(
    title="SentryOps",
    description="DevSecOps Infrastructure Monitoring Platform",
    version="1.0.0",
)

app.include_router(router, prefix="/api/v1")

Instrumentator().instrument(app).expose(app)


@app.get("/")
async def root():
    return {
        "service": "SentryOps",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_url": "/api/v1/health",
        "metrics_url": "/metrics",
    }
