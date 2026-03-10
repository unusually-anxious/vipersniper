import redis, json
r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

def get_listings():
    items=[]
    for k in r.scan_iter("listing:*"):
        try:
            items.append(json.loads(r.get(k)))
        except:
            pass
    return items
