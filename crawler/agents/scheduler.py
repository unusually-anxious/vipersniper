import time
from crawler.core.redis_bus import publish
from crawler.models.jobs import FetchJob

SOURCES = [
    {
        "source_name": "demo_api",
        "source_type": "api",
        "url": "http://127.0.0.1:9000/api/listings",
        "parser_name": "demo_api_parser",
        "interval_seconds": 30,
    }
]


def main():
    while True:
        for source in SOURCES:
            job = FetchJob(
                source_name=source["source_name"],
                source_type=source["source_type"],
                url=source["url"],
                parser_name=source["parser_name"],
            )
            publish("fetch_jobs", job.model_dump())
            print(f"scheduled: {source['source_name']}")
        time.sleep(30)


if __name__ == "__main__":
    main()
