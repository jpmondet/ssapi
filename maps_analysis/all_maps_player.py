#! /usr/bin/env python3

import requests
import json
import pprint
from time import sleep
from argparse import ArgumentParser

def handle_arguments():
    parser = ArgumentParser(
    prog="get_all_maps_player",
    description="Leverage ScoreSaber API to get all the maps a player played since the beginning",
    )

    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="ss url",
        default="https://new.scoresaber.com/api/player/{}/scores/recent/{}",
    )
    parser.add_argument(
        "-p",
        "--player",
        type=str,
        help="Specify the ss id of the player. Exple : 76561198415354041",
    )
    parser.add_argument(
        "-n",
        "--nb-pages",
        type=int,
        help="Number of pages to scrap",
        default=1000,
    )
    args = parser.parse_args()
    
    return args
    
def main():

    args = handle_arguments()

    maps_playah = []

    if not args.player:
        print("Please, specify the ss id of the player with '-p'")
        return 1

    for page in range(1, args.nb_pages):
        print(f"Asking for page {page} / {args.nb_pages}")
        url = (args.url).format(args.player, page)
        print(url)
        req = requests.get(url)
        sleep(1)
        try:
            reqjson = req.json()
            if reqjson.get('error'):
                break
            maps_playah.extend(reqjson["scores"])
        except Exception as expt:
            print(expt)
            continue

    print(maps_playah)

    with open(f'all_maps_players_{args.player}.json', 'w') as fmaps:
        json.dump(maps_playah, fmaps)

if __name__ == "__main__":
    main()
