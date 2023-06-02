import json


not_done = []
for i in range(4000):
    print(i)
    with open(f"sertalp/{i:04d}.json", "r") as f:
        data = json.load(f)
        if "chips" not in data[0]:
            not_done.append(i)
            print(f"---------- sertalp/{i:04d}.json ----------")


print("NOT DONE: ", not_done)
