import aiohttp
import argparse
import asyncio
import json
import os
import random
import sys
import time

from nordvpn_switcher import initialize_VPN, rotate_VPN

# vpn_settings = initialize_VPN(area_input=["random countries europe 20"])

parser = argparse.ArgumentParser()
parser.add_argument("start_chunk", type=int)
parser.add_argument("end_chunk", type=int)
args = parser.parse_args()
TOTAL_PLAYERS = 7_811_694
BASE_FOLDER = "sertalp"


async def fetch(session, url, headers, max_retries=200, cooldown=0.1):
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


async def update_json(session, filename, start_user_id, end_user_id):
    user_ids = list(range(start_user_id, end_user_id + 1))
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "transfers" in data[0]:
        return

    urls = [f"https://fantasy.premierleague.com/api/entry/{user_id}/transfers/" for user_id in user_ids]

    headers = {"User-Agent": f"Android {random.choice(range(7, 30))}.{random.choice(range(4,11))}"}
    tasks = [fetch(session, url, headers) for url in urls]
    results = await asyncio.gather(*tasks)

    for user, result in zip(data, results):
        if result == {"detail": "Not found."}:
            user["transfers"] = []
        else:
            user["transfers"] = [[x["element_out"], x["element_in"], x["event"]] for x in result[::-1]]

    with open(filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(data))


async def main():
    TIME_START = time.time()
    VPN_ROTATE_FREQUENCY = 100

    session = aiohttp.ClientSession()
    # rotate_VPN(vpn_settings)

    # files_dct = {file: os.path.getsize(f"sertalp/{file}") for file in os.listdir(BASE_FOLDER)}
    # files_dct = sorted(files_dct.items(), key=lambda x: x[1])
    # to_do = [int(x[0][:4]) for x in files_dct]
    # print(to_do)

    for chunk_num, i in enumerate(range(args.start_chunk, args.end_chunk), start=1):
        # for chunk_num, i in enumerate(to_do, start=1):
        # if chunk_num % VPN_ROTATE_FREQUENCY == 0:
        #     await session.close()
        #     while True:
        #         try:
        #             rotate_VPN(vpn_settings)
        #             session = aiohttp.ClientSession()
        #             break
        #         except:
        #             pass
        #     time.sleep(1)
        a = time.time()
        n = 1000  # number of users in each file
        start = n * i + 1
        end = TOTAL_PLAYERS if i == TOTAL_PLAYERS // n else start + n - 1

        try:
            await update_json(session, f"{BASE_FOLDER}/{i:04d}.json", start_user_id=start, end_user_id=end)
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
