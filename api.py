from api_patch import get_listings
from api_patch import get_listings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow your frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Demo listing data
LISTINGS = [
    {
        "id":401,
        "external_id":"401",
        "year":2020,
        "make":"Tesla",
        "model":"Model 3",
        "bid":0,
        "score":80,
        "location":"Dallas, TX",
        "damage":"Front",
        "title_status":"Clean",
        "vin":"5YJ3E1EA7LF000001",
        "image_url":"https://images.unsplash.com/photo-1619767886558-efdc259cde1a",
        "url":"https://example.com"
    },
    {
        "id":402,
        "external_id":"402",
        "year":2021,
        "make":"Ford",
        "model":"F-150",
        "bid":500,
        "score":15,
        "location":"Houston, TX",
        "damage":"Rear",
        "title_status":"Clean",
        "vin":"1FTFW1E50MFA00002",
        "image_url":"https://images.unsplash.com/photo-1552519507-da3b142c6e3d",
        "url":"https://example.com"
    }
]

@app.get("/")
def root():
    return {"status":"ViperSniper API running"}

@app.get("/listings")
def get_listings():
    return {"items": LISTINGS}
