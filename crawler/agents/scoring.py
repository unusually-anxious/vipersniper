import json
from crawler.core.redis_bus import consume, ack, publish

STREAM = "listing_events"
GROUP = "scoring"
CONSUMER = "scorer-1"


def score(listing):

    score = 0

    bid = listing.get("bid", 0)
    title = (listing.get("title_status") or "").lower()
    damage = (listing.get("damage") or "").lower()

    if bid == 0:
        score += 50

    if "clean" in title:
        score += 20

    if "rear" in damage:
        score += 10

    if "front" in damage:
        score -= 5

    return max(0, min(100, score))


def main():

    print("scoring worker started")

    while True:

        messages = consume(STREAM, GROUP, CONSUMER)

        if not messages:
            continue

        for stream, entries in messages:

            for msg_id, fields in entries:

                payload = json.loads(fields["data"])
                listing = payload["listing"]

                deal_score = score(listing)
                listing["score"] = deal_score

                print("scored:", listing["external_id"], deal_score)

                publish(
                    "dashboard_events",
                    {
                        "type": "listing_scored",
                        "listing": listing,
                    },
                )

                ack(STREAM, GROUP, msg_id)


if __name__ == "__main__":
    main()
