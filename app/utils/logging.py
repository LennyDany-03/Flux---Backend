from typing import Optional, Tuple

def extract_client_meta(headers, client) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    ip = client.host if client else None
    user_agent = headers.get("user-agent")
    referrer = headers.get("referer") or headers.get("referrer")
    return ip, user_agent, referrer
