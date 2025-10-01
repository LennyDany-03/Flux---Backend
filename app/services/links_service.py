from typing import Any, Dict, List, Optional
from app.db.supabase_client import supabase

LINKS_TABLE = "links"
CLICKS_TABLE = "clicks"

def _one_or_none(resp) -> Optional[Dict[str, Any]]:
    return resp.data[0] if getattr(resp, "data", None) else None

def create_link(*, code: str, destination_url: str, title: Optional[str]) -> Dict[str, Any]:
    # Ensure unique code
    existing = supabase.table(LINKS_TABLE).select("id").eq("code", code).execute()
    if existing.data:
        raise ValueError("Code already exists")
    ins = supabase.table(LINKS_TABLE).insert({
        "code": code,
        "destination_url": destination_url,
        "title": title,
    }).execute()
    return _one_or_none(ins)

def list_links() -> List[Dict[str, Any]]:
    resp = supabase.table(LINKS_TABLE).select("*").order("created_at", desc=True).execute()
    return resp.data or []

def get_link_by_code(code: str) -> Optional[Dict[str, Any]]:
    resp = supabase.table(LINKS_TABLE).select("*").eq("code", code).execute()
    return _one_or_none(resp)

def get_link_by_id(link_id: str) -> Optional[Dict[str, Any]]:
    resp = supabase.table(LINKS_TABLE).select("*").eq("id", link_id).execute()
    return _one_or_none(resp)

def update_link(code: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not updates:
        # Nothing to do; return current
        current = get_link_by_code(code)
        return current
    upd = supabase.table(LINKS_TABLE).update(updates).eq("code", code).execute()
    return _one_or_none(upd)

def delete_link(code: str) -> bool:
    delr = supabase.table(LINKS_TABLE).delete().eq("code", code).execute()
    # supabase-py v2 returns count only if count option set; data presence implies deletion.
    return bool(getattr(delr, "data", None)) or getattr(delr, "count", 0) > 0

def log_click(*, link_id: str, ip: Optional[str], user_agent: Optional[str], referrer: Optional[str]) -> None:
    try:
        supabase.table(CLICKS_TABLE).insert({
            "link_id": link_id,
            "ip": ip,
            "user_agent": user_agent,
            "referrer": referrer,
        }).execute()
    except Exception:
        # best-effort logging; swallow errors
        pass
