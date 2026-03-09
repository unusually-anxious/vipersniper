import json
import os
from dotenv import load_dotenv
from supabase import create_client
from crawler.core.redis_bus import consume, ack

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

STREAM = "dashboard_events"
GROUP = "storage"
CONSUMER = "storage-1"


def main():
    print("storage worker started")

    while True:
        messages = consume(STREAM, GROUP, CONSUMER)

        if not messages:
            continue

        for stream, entries in messages:
            for msg_id, fields in entries:
                try:
                    payload = json.loads(fields["data"])
                    listing = payload["listing"]

                    row = {
                        "source_name": listing.get("source_name"),
                        "external_id": listing.get("external_id"),
                        "url": listing.get("url"),
                        "title": listing.get("title"),
                        "vin": listing.get("vin"),
                        "year": listing.get("year"),
                        "make": listing.get("make"),
                        "model": listing.get("model"),
                        "bid": listing.get("bid"),
                        "buy_now": listing.get("buy_now"),
                        "end_time": listing.get("end_time"),
                        "location": listing.get("location"),
                        "title_status": listing.get("title_status"),
                        "damage": listing.get("damage"),
                        "image_count": listing.get("image_count"),
                        "score": listing.get("score", 0),
                    }

                    supabase.table("listings").upsert(
                        row,
                        on_conflict="source_name,external_id"
                    ).execute()

                    print("saved:", row["external_id"])
                    ack(STREAM, GROUP, msg_id)

                except Exception as e:
                    print("storage error:", e)


if __name__ == "__main__":
    main()
