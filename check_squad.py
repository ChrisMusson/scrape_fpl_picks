import json
import requests
import sys

USER_ID = 798
BASE_FOLDER = "sertalp/"

with open(f"{BASE_FOLDER}{USER_ID // 1000:04d}.json", "r") as f:
    file_data = json.load(f)[USER_ID % 1000 - 1]["picks"]

gws = [x for x in file_data]
# print(gws)
# print(file_data)

live_data = {}
with requests.Session() as s:
    for gw in gws:
        r = s.get(f"https://fantasy.premierleague.com/api/entry/{USER_ID}/event/{gw}/picks/").json()
        live_data[gw] = [[x["element"], x["multiplier"]] for x in r["picks"]]

for gw in gws:
    file = [x[0] for x in file_data[gw]]
    live = [x[0] for x in live_data[gw]]
    file_cap = [x for x in file_data[gw] if x[1] > 1][0]
    print(file)
    print(live)
    print(gw, file_cap)
    if file != live:
        print("BROKEN", gw, file, live)
        sys.exit(0)
print("GOOD")
