import os
import json
import importlib
from crawler.core.redis_bus import consume, ack, publish

STREAM_IN = "raw_pages"
GROUP = "parsers"
CONSUMER = f"parser-{os.getpid()}"



def load_parser(parser_name: str):
    module = importlib.import_module(f"crawler.parsers.{parser_name}")
    class_name = "".join(part.capitalize() for part in parser_name.split("_"))
    return getattr(module, class_name)()


def main():
    while True:
        messages = consume(STREAM_IN, GROUP, CONSUMER)

        if not messages:
            continue

        for stream_name, entries in messages:
            for msg_id, fields in entries:
                payload = json.loads(fields["data"])

                try:
                    parser = load_parser(payload["parser_name"])
                    records = parser.parse(payload)

                    for record in records:
                        publish("parsed_records", record)

                    ack(STREAM_IN, GROUP, msg_id)
                    print("parsed:", payload["url"])
                except Exception as e:
                    print("parse error:", e)


if __name__ == "__main__":
    main()
