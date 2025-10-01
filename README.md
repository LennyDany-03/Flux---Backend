# Redirector API (FastAPI + Supabase)

## Features
- Create shortlinks (code → destination_url)
- Update destination later (same code)
- 307 redirects + click logging
- QR PNG generation for each code
- CORS for your Next.js admin

## Run
1. Copy `.env.example` → `.env` and fill `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY`.
2. Install deps:
   ```bash
   pip install -e .
   # or: pip install fastapi "uvicorn[standard]" python-dotenv pydantic pydantic-settings supabase "qrcode[pil]"
