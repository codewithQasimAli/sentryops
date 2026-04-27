from fastapi import APIRouter, HTTPException

from app.core.monitor import HealthMonitor

router = APIRouter()
monitor = HealthMonitor()


@router.get("/health")
async def health():
    return {"status": "ok", "service": "SentryOps"}


@router.get("/check")
async def check_all():
    results = await monitor.check_all()
    healthy = sum(1 for r in results if r["status"] == "healthy")
    return {
        "summary": {
            "total": len(results),
            "healthy": healthy,
            "unhealthy": len(results) - healthy,
        },
        "results": results,
    }


@router.get("/check/{target_name}")
async def check_target(target_name: str):
    target = next(
        (t for t in monitor.targets if t["name"].lower() == target_name.lower()),
        None,
    )
    if target is None:
        available = [t["name"] for t in monitor.targets]
        raise HTTPException(
            status_code=404,
            detail=f"Target '{target_name}' not found. Available targets: {available}",
        )
    result = await monitor.check_endpoint(target["name"], target["url"])
    return result
