import io
import qrcode
from app.core.config import settings

def build_redirect_url(code: str) -> str:
    base = settings.API_BASE_URL.rstrip("/")
    return f"{base}/l/{code}"           # new: interstitial landing first

def generate_qr_png(code: str) -> bytes:
    url = build_redirect_url(code)
    img = qrcode.make(url)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
