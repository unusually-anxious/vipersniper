from fastapi import FastAPI

app = FastAPI()


@app.get("/api/listings")
def listings():
    return {
        "results": [
            {
                "id": 401,
                "url": "https://example.com/listing/1",
                "title": "2020 Tesla Model 3 Long Range",
                "vin": "5YJ3E1EB7LF000291",
                "year": 2020,
                "make": "Tesla",
                "model": "Model 3",
                "bid": 0,
                "buy_now": None,
                "end_time": "2026-03-08T18:00:00Z",
                "location": "Dallas, TX",
                "title_status": "Clean",
                "damage": "Rear",
                "image_count": 12
            },
            {
                "id": 402,
                "url": "https://example.com/listing/2",
                "title": "2021 Ford F-150 XLT 4x4",
                "vin": "1FTFW1E83MFA87412",
                "year": 2021,
                "make": "Ford",
                "model": "F-150",
                "bid": 500,
                "buy_now": None,
                "end_time": "2026-03-08T19:30:00Z",
                "location": "Houston, TX",
                "title_status": "Clean",
                "damage": "Front",
                "image_count": 8
            }
        ]
    }
