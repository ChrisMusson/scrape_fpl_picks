import json
import random
import requests
import sys


team_map = {
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


user_ids = random.sample(range(1, 50000), 10)
BASE_FOLDER = "sertalp"

# user_ids = [1167]

for user_id in user_ids:
    print(user_id)
    with open(f"{BASE_FOLDER}/{(user_id - 1) // 1000:04d}.json", "r") as f:
        file_data = json.load(f)[user_id % 1000 - 1]
        file_details = [
            file_data["first_name"],
            file_data["second_name"],
            file_data["region"],
            file_data["favourite_team"],
            file_data["total_points"],
            file_data["overall_rank"],
            file_data["team_name"],
        ]
        # file_details = sorted(file_details)

    with requests.Session() as s:
        live_user = s.get(f"https://fantasy.premierleague.com/api/entry/{user_id}/").json()
        live_details = [
            live_user["player_first_name"],
            live_user["player_last_name"],
            live_user["player_region_name"],
            team_map[live_user["favourite_team"]],
            live_user["summary_overall_points"],
            live_user["summary_overall_rank"],
            live_user["name"],
        ]
        # live_details = sorted(live_details)
        # print(json.dumps(file_data, indent=2))
        # print(json.dumps(live_chips, indent=2))
    # print(user_id)
    # print(file_data)

    print(live_details, file_details, live_details == file_details)
