import json
import random
import requests
import sys

user_ids = random.sample(range(1, 10000), 100)
BASE_FOLDER = "sertalp"

user_ids = [1167]

for user_id in user_ids:
    with open(f"{BASE_FOLDER}/{(user_id - 1) // 1000:04d}.json", "r") as f:
        file_data = json.load(f)[user_id % 1000 - 1]["chips"]

    with requests.Session() as s:
        live_chips = s.get(f"https://fantasy.premierleague.com/api/entry/{user_id}/history/").json()["chips"]
        # print(json.dumps(file_data, indent=2))
        # print(json.dumps(live_chips, indent=2))
    print(user_id)
    print(file_data)
    a = sorted(list(file_data.values()))
    b = sorted([x["event"] for x in live_chips])

    print(a, b, a == b)
