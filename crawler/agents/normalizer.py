import json
from crawler.core.redis_bus import consume, ack, publish
from crawler.models.listing import Listing

STREAM_IN = "parsed_records"
GROUP = "normalizers"
CONSUMER = "normalizer-1"


def main():
    while True:
        messages = consume(STREAM_IN, GROUP, CONSUMER)

        if not messages:
            continue

        for stream_name, entries in messages:
            for msg_id, fields in entries:
                payload = json.loads(fields["data"])

                try:
                    listing = Listing(**payload)
                    publish("normalized_records", listing.model_dump())
                    ack(STREAM_IN, GROUP, msg_id)
                    print("normalized:", listing.external_id)
                except Exception as e:
                    print("normalize error:", e)


if __name__ == "__main__":
    main()
