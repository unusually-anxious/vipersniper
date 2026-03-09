import json
import hashlib
from redis import Redis
from crawler.core.redis_bus import consume, ack, publish

redis_client = Redis(host="127.0.0.1", port=6379, decode_responses=True)

STREAM_IN = "normalized_records"
GROUP = "dedupe"
CONSUMER = "dedupe-1"


def listing_key(payload: dict) -> str:
    return f"{payload['source_name']}:{payload['external_id']}"


def fingerprint(payload: dict) -> str:
    important = {
        "bid": payload.get("bid"),
        "buy_now": payload.get("buy_now"),
        "end_time": payload.get("end_time"),
        "title_status": payload.get("title_status"),
        "damage": payload.get("damage"),
    }
    return hashlib.sha256(json.dumps(important, sort_keys=True).encode()).hexdigest()


def main():
    while True:
        messages = consume(STREAM_IN, GROUP, CONSUMER)

        if not messages:
            continue

        for stream_name, entries in messages:
            for msg_id, fields in entries:
                payload = json.loads(fields["data"])

                try:
                    key = listing_key(payload)
                    new_fp = fingerprint(payload)
                    old_fp = redis_client.get(f"fp:{key}")

                    if old_fp is None:
                        event_type = "new_listing"
                    elif old_fp != new_fp:
                        event_type = "changed_listing"
                    else:
                        event_type = "unchanged"

                    if event_type != "unchanged":
                        redis_client.set(f"fp:{key}", new_fp)
                        redis_client.set(f"listing:{key}", json.dumps(payload))

                        publish("listing_events", {
                            "event_type": event_type,
                            "listing": payload,
                        })

                    ack(STREAM_IN, GROUP, msg_id)
                    print("dedupe:", key, event_type)
                except Exception as e:
                    print("dedupe error:", e)


if __name__ == "__main__":
    main()
