#! /usr/bin/env python3

import os
import encodings.idna
import asyncio
import aiohttp
import time
import json

url = "https://new.scoresaber.com/api/players/"

lock = asyncio.Lock()
infos = {}
threads = 20
sleep_time = 3

async def get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with asyncio.Semaphore(threads):
                #async with session.get(url=url) as response:
                #    return await response.json(encoding="utf-8")
                resp = await session.get(url=url)
                async with resp:
                    if resp.status == 200:
                        return await resp.json(encoding="utf-8")
                    rtext = await resp.text()
                    print("Oops issue here :( ", rtext)
    except Exception as e:
        print("Unable to get url {} due to {}. Details : {}".format(url, e.__class__, e))

async def scrapping_urls(urls, file_to_store):
    # Artificially slows polling since ssapi is rate-limiting..
    if len(urls) > threads:
        loops = int(len(urls) / threads)
        remaining = len(urls) % threads
        #print(loops,remaining)

        start = 0
        stop = threads
        for loop in range(loops):
            #print(len(urls[start:stop]), start, stop)
            ret_list = await asyncio.gather(*[get(url) for url in urls[start:stop]])
            async with lock:
                for count, ret in enumerate(ret_list):
                    infos[count+start] = ret
            start = stop
            if stop + threads > len(urls):
                stop = len(urls)
            else:
                stop = stop + threads
            time.sleep(sleep_time)
        if remaining:
            #print(len(urls[start:stop+remaining]), start, stop, remaining)
            ret_list = await asyncio.gather(*[get(url) for url in urls[start:stop + remaining]])
            async with lock:
                for count, ret in enumerate(ret_list):
                    infos[count+start] = ret

        with open(file_to_store, "w") as fpage:
            json.dump(infos, fpage, indent=2)
    else:
        ret_list = await asyncio.gather(*[get(url) for url in urls])
        async with lock:
            for count, ret in enumerate(ret_list):
                infos[count] = ret
        with open(file_to_store, "w") as fpage:
            json.dump(infos, fpage, indent=2)

def parallel_url_scrapping(urls, file_to_store):
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(scrapping_urls(urls, file_to_store))
    finally:
        loop.close()

def main():
    nb_pages = 112
    urls = [url+str(page) for page in range(1, nb_pages)]
    parallel_url_scrapping(urls, "tmp_file.json")



if __name__ == "__main__":
    main()
