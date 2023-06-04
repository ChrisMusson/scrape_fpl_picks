import json


for i in range(4000):
    print(i)
    with open(f"sertalp/{i:04d}.json", "r") as f:
        data = json.load(f)

    if sorted([int(x) for x in data[0]["picks"].keys()]) != list(range(1, 39)):
        print([int(x) for x in data[0]["picks"].keys()])
        for user in data:
            user["picks"] = dict(sorted(user["picks"].items(), key=lambda x: int(x[0])))
        with open(f"sertalp/{i:04d}.json", "w") as f:
            f.write(json.dumps(data))
