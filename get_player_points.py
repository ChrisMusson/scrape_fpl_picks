import json
import requests


player_points_data = {}


def get_player_points(s, player_id, player_points_data):
    print(player_id)
    player_points_data[player_id] = {str(i): 0 for i in range(1, 39)}
    r = s.get(f"https://fantasy.premierleague.com/api/element-summary/{player_id}/").json()["history"]
    for match in r:
        player_points_data[player_id][str(match["round"])] += match["total_points"]


with requests.Session() as s:
    players = s.get("https://fantasy.premierleague.com/api/bootstrap-static/").json()["elements"]
    players = sorted(players, key=lambda x: x["id"])
    for player in players:
        get_player_points(s, player["id"], player_points_data)

with open("player_points.json", "w") as f:
    f.write(json.dumps(player_points_data, indent=4))
