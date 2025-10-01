from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from app.services import links_service
from app.services.qr_service import build_redirect_url
from app.core.config import settings

router = APIRouter()

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Redirecting… /{code}</title>
  <style>
    :root {{ color-scheme: light dark; }}
    body {{
      margin: 0; font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
      background: #0b1220; color: #e5e7eb; display:flex; min-height:100vh; align-items:center; justify-content:center;
    }}
    .card {{
      width: min(680px, 92vw); padding: 24px; border-radius: 16px;
      background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
      box-shadow: 0 10px 40px rgba(0,0,0,.35);
    }}
    .title {{ font-weight: 700; font-size: 20px; margin: 0 0 6px; }}
    .muted {{ color: #94a3b8; font-size: 13px; }}
    .row {{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-top:12px; }}
    .chip {{ font-size:12px; padding:4px 8px; border-radius:9999px; border:1px solid rgba(255,255,255,.14); }}
    .btn {{
      padding: 8px 14px; border-radius: 12px; border: 1px solid rgba(255,255,255,.14);
      background: rgba(255,255,255,.05); color: inherit; cursor: pointer;
    }}
    .btn:hover {{ background: rgba(255,255,255,.1); }}
    .progress {{ height: 6px; border-radius: 9999px; background: rgba(255,255,255,.12); margin-top: 16px; overflow:hidden; }}
    .bar {{ height: 100%; width: 30%; background: linear-gradient(90deg, #60a5fa, #6366f1); animation: load 1.4s infinite; }}
    @keyframes load {{
      0% {{ transform: translateX(-30%);}}
      50% {{ transform: translateX(60%);}}
      100% {{ transform: translateX(130%);}}
    }}
    a {{ color:#93c5fd; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="title">/{code}</div>
    <div class="muted" id="status">Checking link status…</div>
    <div class="progress"><div class="bar"></div></div>
    <div class="row">
      <span class="chip">Permanent link</span>
      <span class="chip" id="activeChip">status: —</span>
    </div>
    <div class="row">
      <button class="btn" id="openNow" style="display:none;">Open now</button>
      <a class="btn" href="{qr_url}" target="_blank" rel="noopener">QR</a>
      <button class="btn" id="copy" type="button">Copy URL</button>
    </div>
  </div>

<script>
const code = {code_json};
const apiBase = {api_base_json};
const redirectUrl = {redirect_url_json};
const statusEl = document.getElementById('status');
const chip = document.getElementById('activeChip');
const openBtn = document.getElementById('openNow');

document.getElementById('copy').onclick = async () => {{
  await navigator.clipboard.writeText(window.location.href);
}};

openBtn.onclick = () => {{ window.location.href = redirectUrl; }};

async function check() {{
  try {{
    const res = await fetch(`${{apiBase}}/links/${{code}}`, {{ cache: 'no-store' }});
    if (!res.ok) throw new Error('not found');
    const link = await res.json();
    const active = !!link.is_active;
    chip.textContent = `status: ${{active ? 'active' : 'inactive'}}`;

    if (active && link.destination_url) {{
      statusEl.textContent = 'Destination ready. Redirecting…';
      setTimeout(() => window.location.href = redirectUrl, 600);
      openBtn.style.display = 'inline-flex';
      return true;
    }} else {{
      statusEl.textContent = 'This link will go live soon. Keep this page open; it will redirect automatically once ready.';
      openBtn.style.display = 'none';
      return false;
    }}
  }} catch (e) {{
    statusEl.textContent = 'Link not found or unavailable.';
    chip.textContent = 'status: unavailable';
    openBtn.style.display = 'none';
    return false;
  }}
}}

(async () => {{
  let ok = await check();
  if (!ok) setInterval(check, 3000);
}})();
</script>
</body>
</html>
"""

@router.get("/l/{code}", response_class=HTMLResponse)
def landing(code: str):
    redirect_url = build_redirect_url(code)  # /r/{code}
    qr_url = f"{settings.API_BASE_URL.rstrip('/')}/qr/{code}"

    html = HTML_TEMPLATE.format(
        code=code,
        qr_url=qr_url,
        code_json=f'"{code}"',
        api_base_json=f'"{settings.API_BASE_URL.rstrip("/")}"',
        redirect_url_json=f'"{redirect_url}"',
    )
    return HTMLResponse(content=html)
