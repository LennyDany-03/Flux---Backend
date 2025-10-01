from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from app.services import links_service
from app.services.qr_service import generate_qr_png

router = APIRouter()

@router.get("/{code}")
def qr_png(code: str):
    link = links_service.get_link_by_code(code)
    if not link:
        raise HTTPException(status_code=404, detail="Not found")
    png = generate_qr_png(code)
    return Response(content=png, media_type="image/png")
