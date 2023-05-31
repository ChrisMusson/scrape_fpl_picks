import json
import requests

N = 1000  # num users per file

with open("captain_blanks.json", "r") as f:
    user_captain_blanks = json.load(f)

with open("player_points.json", "r") as f:
    player_points = json.load(f)

with requests.Session() as s:
    for i in range(4000):
        if str(i * 1000 + 1) in user_captain_blanks:
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
            capt_blanks = []
            picks = data[j]["picks"]
            for gw, lineup in picks.items():
                try:
                    cap = [x for x in lineup if x[1] > 1][0]
                    pts = player_points[str(cap[0])][str(gw)]
                    mult = cap[1]
                    if mult == 2:
                        if pts < 7:
                            capt_blanks.append(gw)
                    if mult == 3:
                        if pts < 10:
                            capt_blanks.append(gw)
                except IndexError:
                    capt_blanks.append(gw)
                    # print(user_id, gw)  # user didn't have a playing captain for this gameweek so can just ignore
                    continue
            user_captain_blanks[user_id] = capt_blanks

user_captain_blanks = dict(sorted(user_captain_blanks.items(), key=lambda x: (len(x[1]), int(x[0]))))
with open("captain_blanks.json", "w") as f:
    f.write(json.dumps(user_captain_blanks))
