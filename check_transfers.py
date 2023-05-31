import json
import random
import requests
import sys

user_ids = random.sample(range(1, 30000), 50)
BASE_FOLDER = "sertalp"

user_ids = [53555]

for user_id in user_ids:
    with open(f"{BASE_FOLDER}/{(user_id - 1) // 1000:04d}.json", "r") as f:
        file_data = json.load(f)[user_id % 1000 - 1]["transfers"]

    with requests.Session() as s:
        r = s.get(f"https://fantasy.premierleague.com/api/entry/{user_id}/transfers/").json()
        live_data = [[x["element_out"], x["element_in"], x["event"]] for x in r[::-1]]

    for f, l in zip(file_data, live_data):
        print(f)
        if f != l:
            print("BIG FUCKING PROBLEM")
            sys.exit(0)

    print("woop")
