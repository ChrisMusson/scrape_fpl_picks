import aiohttp
import asyncio
import json
import time
import argparse


# parser = argparse.ArgumentParser()
# parser.add_argument("start_chunk", type=int)
# parser.add_argument("end_chunk", type=int)
# args = parser.parse_args()

HEADERS = {"User-Agent": "Android 5.1"}

async def fetch(session, url, retries=200, cooldown=0.1):
    retries_count = 0
    while True:
        try:
            async with session.get(url, headers=HEADERS) as response:
                result = await response.json()
                return result
        except aiohttp.client_exceptions.ContentTypeError:
            retries_count += 1
            if retries_count > retries:
                raise Exception(
                    f"Could not fetch {url} after {retries} retries")
            if cooldown:
                await asyncio.sleep(cooldown)


async def update_json(session, filename, start_user_id, end_user_id, current_gw):
    user_ids = list(range(start_user_id, end_user_id + 1))
    gws = range(1, current_gw + 1)
    urls = [f"https://fantasy.premierleague.com/api/entry/{user_id}/event/{gw}/picks/" for user_id in user_ids for gw in gws]
    tasks = [fetch(session, url) for url in urls]
    results = await asyncio.gather(*tasks)

    data = []
    for i, user_id in enumerate(user_ids):
        user_data = {}
        user_data["id"] = user_id
        for result in results[i * len(gws):(i + 1) * len(gws)]:
            user_data["picks"] = {gw: [[x["element"], x["multiplier"]] for x in result["picks"]] for gw in gws}
        data.append(user_data)

    with open(filename, "w") as f:
        f.write(json.dumps(data, indent=2))


async def main():
    # async with aiohttp.ClientSession() as session:
    #     bootstrap = fetch(session, "https://fantasy.premierleague.com/api/bootstrap-static/")
    #     current_gw = next([x for x in bootstrap["events"] if x["is_current"]])
    current_gw = 34

    TIME_START = time.time()
    # missed = [106, 145, 148, 164, 173, 175, 176, 189, 195, 214, 220]
    # for i in range(args.start_chunk, args.end_chunk):
    for i in [636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 670, 678, 705, 717, 728, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 880, 883, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999]:
        async with aiohttp.ClientSession() as session:
            a = time.time()
            n = 1000  # number of users in each file
            start = n * i + 1
            end = start + n - 1
            try:
                await update_json(session, f"sertalp/squads_{i:04d}.json", start_user_id=start, end_user_id=end, current_gw=current_gw)
                t = time.time()
                print(f"Success: {start} - {end}, {round(t - a, 1)}s taken - {round(t - TIME_START, 1)}s total - {time.strftime('%H:%M:%S', time.gmtime())}")
            except Exception as e:
                print(e)
        time.sleep(5)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
