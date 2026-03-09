from fastapi import APIRouter

router = APIRouter()

demo_listings = [
{
"id":1,
"title":"2020 Tesla Model 3 Long Range",
"location":"Dallas, TX",
"price":0,
"score":80,
"source":"demo_api",
"image":"https://images.unsplash.com/photo-1617788138017-80ad40651399"
},
{
"id":2,
"title":"2021 Ford F150 XLT 4x4",
"location":"Houston, TX",
"price":500,
"score":15,
"source":"demo_api",
"image":"https://images.unsplash.com/photo-1609521263047-f8f205293f24"
}
]

@router.get("/listings")
def get_listings():
    return demo_listings
