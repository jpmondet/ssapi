#! /usr/bin/env python3

from sys import exit
from os import access, R_OK
from signal import signal, SIGUSR1, Signals
from time import sleep
from argparse import ArgumentParser, Namespace
from json import load, dump
from collections import defaultdict
from typing import Sequence, Dict, Union, Any, DefaultDict, cast
from types import FrameType
import requests

# Types definitions
PinfosType = Dict[str, Union[str, int, float]]
IndexedPinfosType = Dict[int, PinfosType]
JsonType = Dict[str, Any]
FeedInfosType = Dict[str, Union[str, int, float, JsonType]]
SnipzType = DefaultDict[int,Dict[int,int]]

# Global vars
SNIPZ: SnipzType = defaultdict(dict)

def handle_arguments() -> Namespace:
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

def reindex_pinfos_for_fast_processing(pinfos: str) -> IndexedPinfosType:
    if not pinfos:
        print("pinfos arg is necessary")
        exit(1)

    with open(pinfos, 'r') as fpinfos:
        jpinfos: Sequence[PinfosType] = load(fpinfos)

    fast_pinfos: IndexedPinfosType = {}
    for pinfos_map in jpinfos:
        leaderboardid: int = cast(int, pinfos_map['leaderboardId'])
        fast_pinfos[leaderboardid] = pinfos_map
    return fast_pinfos

def check_scores(feed_infos: Sequence[FeedInfosType], pinfos: IndexedPinfosType) -> None:
    global SNIPZ

    for infos in feed_infos:
        leaderboardid: int = cast(int, infos['leaderboardId'])

        if pinfos.get(leaderboardid):
            if infos['flag'] != "fr.png":
                continue
            if infos['playerId'] == 76561197964179685 :
                continue
            str_score = cast(str,infos['score'])
            foreign_score: int = int(str_score.replace(',', ""))
            playerid: int = cast(int, infos['playerId'])
            if SNIPZ.get(playerid):
                try:
                    if SNIPZ[playerid][leaderboardid] == foreign_score:
                        continue
                except KeyError:
                    if not SNIPZ[playerid]:
                        del(SNIPZ[playerid])
            pscore: int = int(pinfos[leaderboardid]['score'])
            if foreign_score > pscore:
                map_metadata: JsonType = cast(JsonType,infos['info'])
                if map_metadata["ranked"] != "Ranked":
                    # Not interested in unranked for now
                    continue
                title: str = map_metadata['title']
                output = f"{infos['name']} | {leaderboardid} ({title}) | {foreign_score} > {pscore}"
                print(output)
                SNIPZ[playerid][leaderboardid] = foreign_score
                with open('snipz', 'a+') as jsnip:
                    jsnip.write(output + '\n')
                with open('snipez.json', 'w') as jsnip:
                    dump(SNIPZ, jsnip)

def flush_snip(signum: Signals, stack: FrameType) -> None:
    print('Signal received, we flush snipz')
    global SNIPZ
    print(SNIPZ)
    SNIPZ = defaultdict(dict)
    print(SNIPZ)


def main() -> None:

    # Register signal
    signal(SIGUSR1, flush_snip)

    args: Namespace = handle_arguments()

    #TODO: Allow to watch for multiple players
    pinfos: IndexedPinfosType = reindex_pinfos_for_fast_processing(args.pinfos)
 
    if access('snipez.json', R_OK):
        global SNIPZ
        with open('snipez.json') as jsnip:
            SNIPZ = load(jsnip)
            SNIPZ = defaultdict(dict, SNIPZ)

    update: int = 1

    while True:
        if update % 86400 == 0:
            print("It's been 24h already :o Updating pinfos...")
            pinfos = reindex_pinfos_for_fast_processing(args.pinfos)

        try:
            req = requests.get(args.url)
            reqjson = req.json()
            if not isinstance(reqjson, list):
                print("Not a list, ss rate-limited us... missed this loop and waiting 10 secs :-(")
                sleep(10)
                continue
        except Exception as expt:
            print(f"Missed this loop due to {expt}:-(")
            print(req)
            print(req.text)
        check_scores(reqjson, pinfos)
        sleep(1)
        update += 1

if __name__ == "__main__":
    main()
