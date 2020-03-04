#! /usr/bin/env python3

import os
import encodings.idna
import asyncio
import aiohttp
import time
import json

url = "https://new.scoresaber.com/api/players/"

infos = {}

async def get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json(encoding="utf-8")
    except Exception as e:
        print("Unable to get url {} due to {}. Details : {}".format(url, e.__class__, e))

async def scrapping_urls(urls, file_to_store):
    ret_list = await asyncio.gather(*[get(url) for url in urls])
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
    nb_pages = 30
    urls = [url+str(page) for page in range(1, nb_pages)]
    parallel_url_scrapping(urls, "tmp_file.json")



if __name__ == "__main__":
    main()
