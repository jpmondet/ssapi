#! /usr/bin/env python3

from os import access, R_OK
from pathlib import Path
from argparse import ArgumentParser
import requests
import json
import pprint

from api_scrapping import parallel_url_scrapping

url = "https://new.scoresaber.com/api/players/"

nb_players_country = {}
tot_scores_country = {}
moy_scores_country = {}
infos_pages = {}


def get_pages_infos(nb_pages):

    for page in range(1,nb_pages):
        req = requests.get(url + str(page))
        res = json.loads(req.text)
        infos_pages[page] = res
        for player in res:
            try:
                nb_players_country[player["country"]] += 1
            except KeyError:
                nb_players_country[player["country"]] = 1
    
    with open('nb_players_country.json', 'w') as fnb:
        json.dump(nb_players_country, fnb, indent=2)
    with open('infos_per_pages.json', 'w') as finfos:
        json.dump(infos_pages, finfos, indent=2)


def get_countries_from_top_n(nb_players, sorted_infos_pages):

    countries_in_top_n = set()

    for page, scores in sorted_infos_pages:
        if nb_players < 50 and int(page) > 1:
            break
        if int(page) > int(nb_players/50) and nb_players >= 50:
            break
        for player in scores:
            if not player["country"]:
                continue
            if player["inactive"] == 1:
                continue
            countries_in_top_n.add(player["country"])

    return countries_in_top_n


def moy_top_n_players_from_countries_in_top_n(top_n_players, nb_players_to_check, sorted_infos_pages):

    set_of_countries_in_top_n = get_countries_from_top_n(nb_players_to_check, sorted_infos_pages)

    for _, scores in sorted_infos_pages:
        for player in scores:
            if player["country"] not in set_of_countries_in_top_n:
                continue
            if not player["country"]:
                continue
            if player["inactive"] == 1:
                continue
            try:
                if nb_players_country[player["country"]] >= top_n_players:
                    continue
                nb_players_country[player["country"]] += 1
                tot_scores_country[player["country"]] += float(player["pp"])
            except KeyError:
                nb_players_country[player["country"]] = 1
                tot_scores_country[player["country"]] = float(player["pp"])
    
    for country, nb_players in nb_players_country.items():
        if nb_players != top_n_players:
            continue
        moy_scores_country[country] = tot_scores_country[country] / nb_players_country[country] 
    
    return sorted(
        moy_scores_country.items(), key=lambda kv: kv[1], reverse=True
    )

def handle_arguments():
    parser = ArgumentParser(
    prog="top_n",
    description="Leverage ScoreSaber API to calculte the PP average of the top N players of each countries \
            appearing in the global top M players ",
    )
    parser.add_argument(
        "-N",
        "--topN",
        type=int,
        help="Will calculate the average of the N players being at the top of their country (15 by default)",
        default=15,
    )
    parser.add_argument(
        "-M",
        "--topM",
        type=int,
        help="Will check the countries appearing in the global top M players to do its calculation (100 by default)",
        default=100,
    )
    parser.add_argument(
        "-u",
        "--update",
        type=int,
        help="If this flag is passed with a number > 0, the script will poll the ScoreSaber API to get the number of pages \
            specified before calculation (MAY BE LONG) \
            (by default, the flag is set to 0 which means that it won't poll the API and try to use the default stored file)",
        default=0,
    )
    parser.add_argument(
        "-f",
        "--filestorage",
        type=str,
        help="Specifies the file countaining already retrieved datas from the API (polling the API being long, we avoid \
                doing it every time). \
                (by default, the stored file is '/tmp/ssaber_pages_data.json')",
        default="/tmp/ssaber_pages_data.json",
    )
    args = parser.parse_args()
    
    return args
    
def main():

    args = handle_arguments()

    if not access(args.filestorage, R_OK):
        if args.update:
            Path(args.filestorage).touch()
        else:
            print(
                "The file {} is not readable.\nDid you already launched the script with -u X (X being the number of pages) ?".format(
                    args.filestorage
                )
            )
            exit()

    top_n_players = args.topN
    nb_players_to_check = args.topM
    if args.update:
        if args.update > 200:
            #TODO Handle the case where there is too much pages at once
            args.update = 200
        urls = [url + str(page) for page in range(1,args.update)]
        parallel_url_scrapping(urls, args.filestorage)

    with open(args.filestorage, 'r') as finfos:
        infos_pages = json.load(finfos)
    
    sorted_pages = sorted(
        infos_pages.items(), key=lambda kv: int(str(kv[0]))
    )

    sorted_moy_scores_country = moy_top_n_players_from_countries_in_top_n(top_n_players, nb_players_to_check, sorted_pages)
    print("PP average of the top{} players from all the countries appearing in the top{}".format(top_n_players, nb_players_to_check))
    for moy in sorted_moy_scores_country:
        print("{}   {:.2f}".format(moy[0], moy[1]))




   
if __name__ == "__main__":
    main()