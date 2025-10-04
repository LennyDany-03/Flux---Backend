from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import links, redirect, qr, landing
import logging

app = FastAPI(title="Redirector API", version="0.1.0")

# Log what we actually loaded for quick CORS debugging
logging.getLogger("uvicorn.error").info(
    f"Allowed origins: {settings.ALLOWED_ORIGINS} | "
    f"Origin regex: {settings.ALLOWED_ORIGIN_REGEX}"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS or ["https://ascendryflux.vercel.app"],
    allow_origin_regex=settings.ALLOWED_ORIGIN_REGEX,   # optional (e.g., "https://.*\\.vercel\\.app")
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(links.router, prefix="/links", tags=["links"])
app.include_router(redirect.router, tags=["redirect"])
app.include_router(qr.router, prefix="/qr", tags=["qr"])
app.include_router(landing.router, tags=["landing"])

# Health
@app.get("/", tags=["health"])
def health():
    return {"ok": True, "service": "redirector", "version": "0.1.0"}

# Debug (safe to remove later)
@app.get("/_debug/origins", tags=["debug"])
def debug_origins():
    return {
        "allow_origins": settings.ALLOWED_ORIGINS,
        "allow_origin_regex": settings.ALLOWED_ORIGIN_REGEX,
    }
