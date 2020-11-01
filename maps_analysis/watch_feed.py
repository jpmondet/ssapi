#! /usr/bin/env python3

from sys import exit
from os import access, R_OK
from time import sleep
from argparse import ArgumentParser
from json import load, dump
from collections import defaultdict
import requests

SNIPZ = defaultdict(dict)

def handle_arguments():
    parser = ArgumentParser(
    prog="WSF",
    description="Watch ss feed for new scores",
    )

    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="ss url",
        default="https://scoresaber.com/scripts/feed.php",
    )
    parser.add_argument(
        "-p",
        "--pinfos",
        type=str,
        help="File containing all infos of a player",
    )
    args = parser.parse_args()
    
    return args

def reindex_pinfos_for_fast_processing(pinfos):
    if not pinfos:
        print("pinfos arg is necessary")
        exit(1)

    with open(pinfos, 'r') as fpinfos:
        jpinfos = load(fpinfos)

    fast_pinfos = {}
    for pinfos_map in jpinfos:
        fast_pinfos[pinfos_map["leaderboardId"]] = pinfos_map
    return fast_pinfos

def check_scores(feed_infos, pinfos):
    global SNIPZ

    for infos in feed_infos:
        if pinfos.get(infos['leaderboardId']):
            if infos['flag'] != "fr.png":
                continue
            if infos['playerId'] == 76561197964179685 :
                continue
            foreign_score = int(infos['score'].replace(',', ""))
            if SNIPZ.get(infos['playerId']):
                try:
                    if SNIPZ[infos['playerId']][infos['leaderboardId']] == foreign_score:
                        continue
                except KeyError:
                    if not SNIPZ[infos['playerId']]:
                        del(SNIPZ[infos['playerId']])
            pscore = int(pinfos[infos['leaderboardId']]['score'])
            if foreign_score > pscore:
                output = f"{infos['name']} | {infos['leaderboardId']} ({infos['info']['title']}) | {foreign_score} > {pscore}"
                print(output)
                SNIPZ[infos['playerId']][infos['leaderboardId']] = foreign_score
                with open('snipz', 'a+') as jsnip:
                    jsnip.write(output + '\n')
                with open('snipez.json', 'w') as jsnip:
                    dump(SNIPZ, jsnip)

    
def main():
    #TODO : enforce type & PYRE checks

    args = handle_arguments()

    #TODO: Allow to watch for multiple players
    pinfos = reindex_pinfos_for_fast_processing(args.pinfos)
 
    if access('snipez.json', R_OK):
        global SNIPZ
        with open('snipez.json') as jsnip:
            SNIPZ = load(jsnip)
            SNIPZ = defaultdict(dict, SNIPZ)

    update = 1

    while True:
        if update % 86400 == 0:
            pinfos = reindex_pinfos_for_fast_processing(args.pinfos)

        req = requests.get(args.url)
        try:
            reqjson = req.json()
            if not isinstance(reqjson, list):
                print("Not a list, ss rate-limited us... missed this loop :-(")
                sleep(10)
                continue
        except Exception as expt:
            print(f"Missed this loop due to {expt}:-(")
        check_scores(reqjson, pinfos)
        sleep(1)
        update += 1

if __name__ == "__main__":
    main()
