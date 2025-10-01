from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.links import LinkCreate, LinkUpdate, LinkOut
from app.services import links_service

router = APIRouter()

@router.post("", response_model=LinkOut)
def create_link(payload: LinkCreate):
    """Create a new shortlink."""
    try:
        created = links_service.create_link(
            code=payload.code,
            destination_url=str(payload.destination_url) if payload.destination_url else None,
            title=payload.title,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    return created


@router.get("", response_model=List[LinkOut])
def list_links():
    """List all shortlinks."""
    return links_service.list_links()


@router.get("/{code}", response_model=LinkOut)
def read_link(code: str):
    """Get a single shortlink by its code."""
    link = links_service.get_link_by_code(code)
    if not link:
        raise HTTPException(status_code=404, detail="Not found")
    return link


@router.patch("/{code}", response_model=LinkOut)
def update_link(code: str, payload: LinkUpdate):
    """Update a shortlink (destination, title, active status)."""
    updates = payload.dict(exclude_unset=True)

    # Cast URL fields to string so they're JSON serializable
    if "destination_url" in updates and updates["destination_url"] is not None:
        updates["destination_url"] = str(updates["destination_url"])

    updated = links_service.update_link(code, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Not found")
    return updated


@router.delete("/{code}")
def delete_link(code: str):
    """Delete a shortlink by its code."""
    ok = links_service.delete_link(code)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": True}
