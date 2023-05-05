import os

done = set(sorted([int(x[7:-5]) for x in os.listdir("sertalp")]))
target = set(range(1000))

to_do = target - done

print(len(to_do))
print(sorted(to_do))