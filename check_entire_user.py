import json
import random
import requests


TEAM_MAP = {
    1: "Arsenal",
    2: "Aston Villa",
    3: "Bournemouth",
    4: "Brentford",
    5: "Brighton",
    6: "Chelsea",
    7: "Crystal Palace",
    8: "Everton",
    9: "Fulham",
    10: "Leicester",
    11: "Leeds",
    12: "Liverpool",
    13: "Man City",
    14: "Man Utd",
    15: "Newcastle",
    16: "Nott'm Forest",
    17: "Southampton",
    18: "Spurs",
    19: "West Ham",
    20: "Wolves",
    None: None,
}
USER_IDS = [53555]
USER_IDS = random.sample(range(1, 23000), 100)
BASE_FOLDER = "sertalp"
HEADERS = {"User-Agent": "Android 15.4"}

# USER_IDS = [53555, 5958429, 6248618, 3094023]


def fetch(s, url):
    return s.get(url, headers=HEADERS).json()


def get_live_user_data(s, user_id):
    data = {
        "id": user_id,
        "picks": {},
        "chips": {"tc": None, "fh": None, "bb": None, "wc1": None, "wc2": None},
    }

    # picks
    for gw in range(1, 39):
        r = fetch(s, f"https://fantasy.premierleague.com/api/entry/{user_id}/event/{gw}/picks/")
        data["picks"][str(gw)] = [[x["element"], x["multiplier"]] for x in r["picks"]]

    # chips
    r = fetch(s, f"https://fantasy.premierleague.com/api/entry/{user_id}/history/")
    for chip in r["chips"]:
        if chip["name"] == "wildcard":
            if chip["event"] <= 16:
                data["chips"]["wc1"] = chip["event"]
            elif chip["event"] > 16:
                data["chips"]["wc2"] = chip["event"]
        elif chip["name"] == "3xc":
            data["chips"]["tc"] = chip["event"]
        elif chip["name"] == "bboost":
            data["chips"]["bb"] = chip["event"]
        elif chip["name"] == "freehit":
            data["chips"]["fh"] = chip["event"]

    # transfers
    r = fetch(s, f"https://fantasy.premierleague.com/api/entry/{user_id}/transfers/")
    data["transfers"] = [[x["element_out"], x["element_in"], x["event"]] for x in r[::-1]]

    # user
    r = fetch(s, f"https://fantasy.premierleague.com/api/entry/{user_id}/")
    data["first_name"] = r["player_first_name"]
    data["second_name"] = r["player_last_name"]
    data["region"] = r["player_region_name"]
    data["favourite_team"] = TEAM_MAP[r["favourite_team"]]
    data["total_points"] = r["summary_overall_points"]
    data["overall_rank"] = r["summary_overall_rank"]
    data["team_name"] = r["name"]

    return data


def get_data_from_file(user_id):
    with open(f"{BASE_FOLDER}/{(user_id - 1) // 1000:04d}.json", "r") as f:
        return json.load(f)[user_id % 1000 - 1]


with requests.Session() as s:
    for user_id in USER_IDS:
        print(f"Checking {user_id} ...")
        live = get_live_user_data(s, user_id)
        file = get_data_from_file(user_id)

        # picks = live["picks"]
        # for x in picks:
        #     print(x, picks[x] == file["picks"][str(x)])

        # print(live == file)
        if not live == file:
            print("----------------------TERRIBLE MISTAKE")
            for gw in range(1, 39):
                l = live["picks"][str(gw)]
                r = file["picks"][str(gw)]
                print(gw, l == r)
