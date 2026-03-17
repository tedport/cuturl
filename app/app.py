from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routers import redirect, links
from app.core.exceptions import register_exception_handlers

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

register_exception_handlers(app)

@app.get("/static/favicon.ico", include_in_schema=False)
async def icon():
    return FileResponse("favicon.ico")
app.include_router(redirect.router)
app.include_router(links.router)