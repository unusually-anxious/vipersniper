import json
from typing import Any
from redis import Redis

redis_client = Redis(host="127.0.0.1", port=6379, decode_responses=True)


def publish(stream: str, payload: dict[str, Any]) -> str:
    return redis_client.xadd(stream, {"data": json.dumps(payload, default=str)})


def ensure_group(stream: str, group: str) -> None:
    try:
        redis_client.xgroup_create(stream, group, id="$", mkstream=True)
    except Exception:
        pass


def consume(stream: str, group: str, consumer: str, count: int = 10, block: int = 5000):
    ensure_group(stream, group)
    return redis_client.xreadgroup(
        groupname=group,
        consumername=consumer,
        streams={stream: ">"},
        count=count,
        block=block,
    )


def ack(stream: str, group: str, message_id: str) -> None:
    redis_client.xack(stream, group, message_id)
