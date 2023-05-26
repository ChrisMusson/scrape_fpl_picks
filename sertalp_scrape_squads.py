import aiohttp
import argparse
import asyncio
import json
import os
import random
import sys
import time

from nordvpn_switcher import initialize_VPN, rotate_VPN

vpn_settings = initialize_VPN(area_input=["random countries europe 20"])

parser = argparse.ArgumentParser()
parser.add_argument("start_chunk", type=int)
parser.add_argument("end_chunk", type=int)
args = parser.parse_args()
TOTAL_PLAYERS = 7_811_694
BASE_FOLDER = "sertalp"


async def fetch(session, url, headers, max_retries=500, cooldown=0.1):
    retries_count = 0
    while True:
        try:
            async with session.get(url, headers=headers) as response:
                return await response.json()
        except aiohttp.client_exceptions.ContentTypeError:
            retries_count += 1
            if retries_count > max_retries:
                raise Exception(f"Could not fetch {url} after {max_retries} retries")
            if cooldown:
                await asyncio.sleep(cooldown)


async def update_json(session, filename, start_user_id, end_user_id, current_gw):
    user_ids = list(range(start_user_id, end_user_id + 1))
    try:
        with open(filename, "r") as f:
            existing_data = json.load(f)
            start_gw = sorted([int(x) for x in existing_data[0]["picks"].keys()])[-1] + 1
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = None
        start_gw = 1

    gws = range(start_gw, current_gw + 1)
    urls = [
        f"https://fantasy.premierleague.com/api/entry/{user_id}/event/{gw}/picks/"
        for user_id in user_ids
        for gw in gws
    ]
    print(f"Getting {len(urls)} urls")

    headers = {"User-Agent": f"Android {random.choice(range(7, 20))}.{random.choice(range(1,4))}"}
    tasks = [fetch(session, url, headers) for url in urls]
    results = await asyncio.gather(*tasks)

    data = []
    for i, user_id in enumerate(user_ids):
        if not existing_data:
            user_data = {}
            user_data["id"] = user_id
            user_data["picks"] = {}
        else:
            user_data = existing_data[i]
        for gw, result in enumerate(results[i * len(gws) : (i + 1) * len(gws)], start=start_gw):
            user_data["picks"][gw] = [[x["element"], x["multiplier"]] for x in result["picks"]]
        data.append(user_data)

    with open(filename, "w") as f:
        f.write(json.dumps(data))


async def main():
    current_gw = 37
    TIME_START = time.time()
    VPN_ROTATE_FREQUENCY = 30

    # done = set(sorted([int(x[:-5]) for x in os.listdir(BASE_FOLDER)]))
    # target = set(range(args.start_chunk, args.end_chunk))
    # to_do = sorted(target - done)
    # print(to_do)
    # print(len(to_do))

    session = aiohttp.ClientSession()
    rotate_VPN(vpn_settings)

    for chunk_num, i in enumerate(range(args.start_chunk, args.end_chunk), start=1):
        # for chunk_num, i in enumerate(to_do, start=1):
        if chunk_num % VPN_ROTATE_FREQUENCY == 0:
            await session.close()
            while True:
                try:
                    rotate_VPN(vpn_settings)
                    session = aiohttp.ClientSession()
                    break
                except:
                    pass
            time.sleep(1)
        a = time.time()
        n = 1000  # number of users in each file
        start = n * i + 1
        end = TOTAL_PLAYERS if i == TOTAL_PLAYERS // n else start + n - 1

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
    await session.close()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
