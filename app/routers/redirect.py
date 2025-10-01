from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from app.services import links_service
from app.utils.logging import extract_client_meta

router = APIRouter()

@router.get("/r/{code}")
def redirect(code: str, request: Request):
    link = links_service.get_link_by_code(code)
    if not link or not link.get("is_active", True):
        raise HTTPException(status_code=404, detail="Inactive or not found")

    ip, ua, ref = extract_client_meta(request.headers, request.client)
    # best-effort logging; ignore failures
    links_service.log_click(link_id=link["id"], ip=ip, user_agent=ua, referrer=ref)

    return RedirectResponse(url=link["destination_url"], status_code=307)
