import aiohttp
import argparse
import asyncio
import json
import os
import time


parser = argparse.ArgumentParser()
parser.add_argument("start_chunk", type=int)
parser.add_argument("end_chunk", type=int)
args = parser.parse_args()
TOTAL_PLAYERS = 7_811_694
HEADERS = {"User-Agent": "Android 14.1"}
BASE_FOLDER = "sertalp"


async def fetch(session, url, max_retries=500, cooldown=0.1):
    retries_count = 0
    while True:
        try:
            async with session.get(url, headers=HEADERS) as response:
                return await response.json()
        except aiohttp.client_exceptions.ContentTypeError:
            retries_count += 1
            if retries_count > max_retries:
                raise Exception(f"Could not fetch {url} after {max_retries} retries")
            if cooldown:
                await asyncio.sleep(cooldown)


async def update_json(session, filename, start_user_id, end_user_id, current_gw):
    user_ids = list(range(start_user_id, end_user_id + 1))
    gws = range(1, current_gw + 1)
    urls = [
        f"https://fantasy.premierleague.com/api/entry/{user_id}/event/{gw}/picks/"
        for user_id in user_ids
        for gw in gws
    ]
    tasks = [fetch(session, url) for url in urls]
    results = await asyncio.gather(*tasks)

    data = []
    for i, user_id in enumerate(user_ids):
        user_data = {}
        user_data["id"] = user_id
        user_data["picks"] = {}
        for gw, result in enumerate(results[i * len(gws) : (i + 1) * len(gws)], start=1):
            user_data["picks"][gw] = [[x["element"], x["multiplier"]] for x in result["picks"]]
        data.append(user_data)

    with open(filename, "w") as f:
        f.write(json.dumps(data))


async def main():
    current_gw = 35
    TIME_START = time.time()

    done = set(sorted([int(x[:-5]) for x in os.listdir(BASE_FOLDER)]))
    target = set(range(args.start_chunk, args.end_chunk))
    to_do = sorted(target - done)

    async with aiohttp.ClientSession() as session:
        for chunk_num, i in enumerate(to_do, start=1):
            a = time.time()
            n = 1000  # number of users in each file
            start = n * i + 1
            end = 7811694 if i == 7811 else start + n - 1

            try:
                await update_json(
                    session,
                    f"{BASE_FOLDER}/{i:04d}.json",
                    start_user_id=start,
                    end_user_id=end,
                    current_gw=current_gw,
                )
                t = time.time()
                ftime = time.strftime("%H:%M:%S", time.localtime())
                print(
                    f"Success: {start} - {end}, {round(t - a, 1)}s taken - {round(t - TIME_START, 1)}s total - {ftime} -- ({chunk_num})"
                )
            except Exception as e:
                print(e)


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
