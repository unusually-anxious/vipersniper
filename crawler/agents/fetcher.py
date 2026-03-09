

import os
import asyncio
import json
from crawler.core.redis_bus import consume, ack, publish
from crawler.core.http_client import client

STREAM_IN = "fetch_jobs"
GROUP = "fetchers"
CONSUMER = f"fetcher-{os.getpid()}"

async def process_job(payload: dict):
    method = payload.get("method", "GET")
    url = payload["url"]
    headers = payload.get("headers", {})
    params = payload.get("params", {})
    body = payload.get("body")

    if method == "POST":
        response = await client.post(url, headers=headers, params=params, json=body)
    else:
        response = await client.get(url, headers=headers, params=params)

    event = {
        "source_name": payload["source_name"],
        "parser_name": payload["parser_name"],
        "url": url,
        "status_code": response.status_code,
        "content_type": response.headers.get("content-type", ""),
        "body": response.text,
    }

    publish("raw_pages", event)


async def main():
    while True:
        messages = consume(STREAM_IN, GROUP, CONSUMER)

        if not messages:
            await asyncio.sleep(1)
            continue

        for stream_name, entries in messages:
            for msg_id, fields in entries:
                payload = json.loads(fields["data"])

                try:
                    await process_job(payload)
                    ack(STREAM_IN, GROUP, msg_id)
                    print("fetched:", payload["url"])
                except Exception as e:
                    print("fetch error:", e)


if __name__ == "__main__":
    asyncio.run(main())
