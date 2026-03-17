from __future__ import annotations

from fastapi import FastAPI


def register(app: FastAPI) -> None:
    @app.get("/api/v1/plugins/example")
    async def plugin_example():
        return {"plugin": "example", "status": "ok"}

