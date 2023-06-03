import json


not_done = []
for i in range(7450, 7812):
    print(i)
    with open(f"sertalp/{i:04d}.json", "r") as f:
        data = json.load(f)
        keys = [
            "first_name",
            "second_name",
            "region",
            "favourite_team",
            "total_points",
            "overall_rank",
            "team_name",
        ]
        if not all([x in data[0] for x in keys]):
            not_done.append(i)
            print(f"---------- sertalp/{i:04d}.json ----------")


print("NOT DONE: ", not_done)
