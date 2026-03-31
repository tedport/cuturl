from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class URLShortenerError(Exception):
    pass

class LinkAccessDeniedError(URLShortenerError):
    pass

class SlugTakenError(URLShortenerError):
    pass

class SlugGenerationError(URLShortenerError):
    pass

class LinkNotFoundError(URLShortenerError):
    pass

class LinkInactiveError(URLShortenerError):
    pass

class LinkExpiredError(URLShortenerError):
    pass

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(LinkNotFoundError)
    async def link_not_found_handler(request: Request, exc: LinkNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": "The requested short link does not exist."},
        )
    @app.exception_handler(LinkInactiveError)
    async def link_inactive_handler(request: Request, exc: LinkInactiveError):
        return JSONResponse(
            status_code=403,
            content={"detail": "This link has been deactivated by the owner."},
        )
    @app.exception_handler(LinkAccessDeniedError)
    async def link_accessdenied_handler(request: Request, exc: LinkInactiveError):
        return JSONResponse(
            status_code=403,
            content={"detail": "Wrong credential provided."},
        )
    @app.exception_handler(LinkExpiredError)
    async def link_expired_handler(request: Request, exc: LinkExpiredError):
        return JSONResponse(
            status_code=410,
            content={"detail": "This link has expired or reached its maximum usage limit."},
        )
    @app.exception_handler(SlugTakenError)
    async def slug_taken_handler(request: Request, exc: SlugTakenError):
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )
    @app.exception_handler(SlugGenerationError)
    async def slug_generation_handler(request: Request, exc: SlugGenerationError):
        return JSONResponse(
            status_code=503,
            content={"detail": "Could not generate a unique shortcut. Please try again."},
        )