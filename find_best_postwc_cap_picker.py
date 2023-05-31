import json

with open("captain_blanks.json", "r") as f:
    data = list(json.load(f).items())

print("done loading")
final = {}
for x, y in data:
    post_wc_blanks = len([a for a in y if int(a) >= 17])
    final[x] = post_wc_blanks


final = dict(sorted(final.items(), key=lambda x: (x[1], x[0]))[:50])
print(final)
