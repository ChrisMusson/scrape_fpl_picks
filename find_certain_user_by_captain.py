import json

N = 1000  # num users per file

wanted = [318, 283, 356, 333, 319]
# wanted = [319]
for i in range(4000):
    # print(i)
    with open(f"sertalp/{i:04d}.json", "r") as f:
        data = json.load(f)

    for j in range(N):
        user_id = i * N + j + 1
        picks = data[j]["picks"]
        caps = []
        for gw, lineup in list(picks.items())[-len(wanted) :]:
            try:
                cap = [x for x in lineup if x[1] > 1][0]
                caps.append(cap[0])
            except IndexError:
                # print(user_id, gw)  # user didn't have a playing captain for this gameweek so can just ignore
                continue
        # print(caps)
        if caps == wanted:
            print(user_id)
