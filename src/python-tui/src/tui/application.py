import asyncio
import pathlib
import signal
from contextlib import asynccontextmanager
from types import ModuleType
from typing import Any

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from tui.routing import configure_app_router

STATIC_FILE_PATH = pathlib.Path(__file__).parent.parent / "static"


class tui(FastAPI):
    def __init__(
        self,
        app: ModuleType,
        **kwargs: Any,
    ) -> None:
        self.default_lifespan = kwargs.pop("default_lifespan", None)
        super().__init__(**kwargs, lifespan=self.lifespan)
        self.app = app
        self.reload = asyncio.Event()
        self.setup_tui()

    def setup_tui(self) -> None:
        app_router = configure_app_router(self.app)
        self.mount("/static", StaticFiles(directory=STATIC_FILE_PATH), name="static")
        self.add_api_route("/_hotreload", self.hotreload, methods=["GET"])
        self.include_router(app_router, tags=["tui"])

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        signal.signal(signal.SIGTERM, self.on_sigterm)
        if self.default_lifespan:
            async with self.default_lifespan(app):
                yield
        else:
            yield

    def on_sigterm(self, *_: Any) -> None:
        self.reload.set()

    async def hotreload(self) -> StreamingResponse:
        async def event_generator():
            try:
                while True:
                    await self.reload.wait()
                    yield "data: reload\n\n"
                    self.reload.clear()
            except asyncio.CancelledError:
                pass

        return StreamingResponse(event_generator(), media_type="text/event-stream")
