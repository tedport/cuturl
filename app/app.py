import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import redirect, links
from app.core.exceptions import register_exception_handlers

app = FastAPI()

register_exception_handlers(app)

app.include_router(redirect.router)
app.include_router(links.router)