import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from .routes.listings import router as listings_router

load_dotenv(".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

app = FastAPI(title="ViperSniper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


@app.get("/")
async def home():
    return FileResponse("frontend/index.html")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/listings")
async def listings():
    result = (
        supabase
        .table("listings")
        .select("*")
        .order("created_at", desc=True)
        .limit(50)
        .execute()
    )
    return {"items": result.data}


@app.get("/zero-bid")
async def zero_bid():
    result = (
        supabase
        .table("listings")
        .select("*")
        .eq("bid", 0)
        .order("created_at", desc=True)
        .limit(50)
        .execute()
    )
    return {"items": result.data}


@app.get("/ending-soon")
async def ending_soon():
    now = datetime.now(timezone.utc)
    soon = now + timedelta(minutes=30)

    result = (
        supabase
        .table("listings")
        .select("*")
        .gte("end_time", now.isoformat())
        .lte("end_time", soon.isoformat())
        .order("end_time", desc=False)
        .limit(50)
        .execute()
    )
    return {"items": result.data}

from fastapi import HTTPException

@app.get("/watchlist")
async def get_watchlist():
    result = supabase.table("watchlist").select("*").order("created_at", desc=True).execute()
    rows = result.data or []

    listing_ids = [row["listing_id"] for row in rows if row.get("listing_id") is not None]
    if not listing_ids:
        return {"items": []}

    listings = supabase.table("listings").select("*").in_("id", listing_ids).execute()
    return {"items": listings.data or []}


@app.post("/watchlist")
async def add_watchlist(payload: dict):
    listing_id = payload.get("listing_id")
    if not listing_id:
        raise HTTPException(status_code=400, detail="listing_id is required")

    existing = supabase.table("watchlist").select("*").eq("listing_id", listing_id).execute()
    if existing.data:
        return {"ok": True, "message": "Already saved"}

    supabase.table("watchlist").insert({"listing_id": listing_id}).execute()
    return {"ok": True}


@app.delete("/watchlist/{listing_id}")
async def remove_watchlist(listing_id: int):
    supabase.table("watchlist").delete().eq("listing_id", listing_id).execute()
    return {"ok": True}


@app.get("/alerts")
async def get_alerts():
    result = supabase.table("alerts").select("*").order("created_at", desc=True).execute()
    return {"items": result.data or []}


@app.post("/alerts")
async def add_alert(payload: dict):
    data = {
        "listing_id": payload.get("listing_id"),
        "keyword": payload.get("keyword"),
        "source_name": payload.get("source_name"),
        "min_score": payload.get("min_score", 0),
        "bid_type": payload.get("bid_type", "all"),
    }
    supabase.table("alerts").insert(data).execute()
    return {"ok": True}


@app.delete("/alerts/{alert_id}")
async def remove_alert(alert_id: int):
    supabase.table("alerts").delete().eq("id", alert_id).execute()
    return {"ok": True}
from .auth import router as auth_router
app.include_router(auth_router)


app.include_router(listings_router)
