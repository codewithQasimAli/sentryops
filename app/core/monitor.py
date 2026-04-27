import asyncio
import time
import httpx


TARGETS = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "AWS", "url": "https://aws.amazon.com"},
    {"name": "Cloudflare", "url": "https://www.cloudflare.com"},
]

TIMEOUT_SECONDS = 5


class HealthMonitor:
    def __init__(self) -> None:
        self.targets = TARGETS

    async def check_endpoint(
        self, name: str, url: str
    ) -> dict:
        start = time.monotonic()
        result: dict = {"name": name, "url": url}
        try:
            async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS, follow_redirects=True) as client:
                response = await client.get(url)
            latency_ms = round((time.monotonic() - start) * 1000, 2)
            result.update(
                {
                    "status": "healthy",
                    "status_code": response.status_code,
                    "latency_ms": latency_ms,
                    "error": None,
                }
            )
        except httpx.TimeoutException:
            latency_ms = round((time.monotonic() - start) * 1000, 2)
            result.update(
                {
                    "status": "unhealthy",
                    "status_code": None,
                    "latency_ms": latency_ms,
                    "error": f"Timeout after {TIMEOUT_SECONDS}s",
                }
            )
        except Exception as exc:
            latency_ms = round((time.monotonic() - start) * 1000, 2)
            result.update(
                {
                    "status": "unhealthy",
                    "status_code": None,
                    "latency_ms": latency_ms,
                    "error": str(exc),
                }
            )
        return result

    async def check_all(self) -> list[dict]:
        tasks = [self.check_endpoint(t["name"], t["url"]) for t in self.targets]
        return await asyncio.gather(*tasks)
