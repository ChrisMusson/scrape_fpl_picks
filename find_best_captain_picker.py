import json
import requests


N = 1000  # num users per file


with open("captain_scores.json", "r") as f:
    user_captain_scores = json.load(f)


with open("player_points.json", "r") as f:
    player_points = json.load(f)


with requests.Session() as s:
    for i in range(4000):
        if str(i * 1000 + 1) in user_captain_scores:
            print(f"Skipping {i}")
            continue

        print(i)
        try:
            with open(f"sertalp/{i:04d}.json", "r") as f:
                data = json.load(f)
        except:
            continue

        for j in range(N):
            user_id = i * N + j + 1
            capt_score = 0
            picks = data[j]["picks"]
            for gw, lineup in picks.items():
                try:
                    cap = [x for x in lineup if x[1] > 1][0]
                    pts = player_points[str(cap[0])][str(gw)]
                    capt_score += pts * cap[1]
                except IndexError:
                    # print(user_id, gw)  # user didn't have a playing captain for this gameweek so can just ignore
                    continue
            user_captain_scores[user_id] = capt_score

user_captain_scores = dict(sorted(user_captain_scores.items(), key=lambda x: (-x[1], int(x[0]))))
with open("captain_scores.json", "w") as f:
    f.write(json.dumps(user_captain_scores))
