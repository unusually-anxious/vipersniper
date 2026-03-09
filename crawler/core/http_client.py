import httpx

client = httpx.AsyncClient(
    timeout=20.0,
    follow_redirects=True,
    http2=True,
    headers={
        "User-Agent": "ViperSniperBot/0.1"
    },
)
