import json
from crawler.sources.base import BaseParser


class DemoApiParser(BaseParser):
    def parse(self, raw_event: dict) -> list[dict]:
        data = json.loads(raw_event["body"])
        results = []

        for item in data.get("results", []):
            results.append({
                "source_name": raw_event["source_name"],
                "external_id": str(item.get("id")),
                "url": item.get("url", ""),
                "title": item.get("title", ""),
                "vin": item.get("vin"),
                "year": item.get("year"),
                "make": item.get("make"),
                "model": item.get("model"),
                "bid": item.get("bid"),
                "buy_now": item.get("buy_now"),
                "end_time": item.get("end_time"),
                "location": item.get("location"),
                "title_status": item.get("title_status"),
                "damage": item.get("damage"),
                "image_count": item.get("image_count"),
            })

        return results
