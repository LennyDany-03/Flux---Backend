from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import links, redirect, qr
from app.routers import landing  # <-- add
app = FastAPI(title="Redirector API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS or ["https://ascendryflux.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(links.router, prefix="/links", tags=["links"])
app.include_router(redirect.router, tags=["redirect"])
app.include_router(qr.router, prefix="/qr", tags=["qr"])
app.include_router(landing.router, tags=["landing"])  # <-- add

@app.get("/", tags=["health"])
def health():
    return {"ok": True, "service": "redirector", "version": "0.1.0"}
