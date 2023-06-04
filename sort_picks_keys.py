import json


for i in range(4000):
    print(i)
    with open(f"sertalp/{i:04d}.json", "r") as f:
        data = json.load(f)
        for user in data:
            user["picks"] = dict(sorted(user["picks"].items(), key=lambda x: int(x[0])))
    with open(f"sertalp/{i:04d}.json", "w") as f:
        f.write(json.dumps(data))
