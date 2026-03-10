from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import datetime

router = APIRouter()

@router.get("/{slug}", response_class=RedirectResponse, status_code=302)
async def cuturl_redirect(slug : str, request : Request):
    record_data = {"slug"		: slug,
                   "timestamp"	: datetime.datetime.now(datetime.timezone.utc),
                   "ip" 		: request.client.host,
                   "device"		: request.headers.get("User-Agent")}
    print(record_data)
    return "https://google.com"