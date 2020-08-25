#! /usr/bin/env python3

import requests
import json
import pprint
from api_scrapping import parallel_url_scrapping

url = "https://new.scoresaber.com/api/player/{}/full"

country = "fr" # "all" for world ranking

players_rankedcount = {}
urls_to_scrap = []
disc = True

with open('ssaber_pages_data.json', 'r') as finfos:
    infos_pages = json.load(finfos)

for _, scores in infos_pages.items():
    for player in scores['players']:
        if player["country"].lower() == country.lower() or country.lower() == "all":
            urls_to_scrap.append(url.format(player["playerId"]))

#print(len(urls_to_scrap))

parallel_url_scrapping(urls_to_scrap, 'infos_players_full.json')

with open('infos_players_full.json', 'r') as finfos:
    infos_players_full = json.load(finfos)


for _, infos in infos_players_full.items():
    players_rankedcount[infos['playerInfo']['playerName']] = (infos['scoreStats']['rankedPlayCount'], infos['scoreStats']['averageRankedAccuracy'])


pcount_rank = sorted(
    players_rankedcount.items(), key=lambda kv: kv[1][0], reverse=True
)
accu_rank = sorted(
    players_rankedcount.items(), key=lambda kv: kv[1][1], reverse=True
)


#print("#"*15, "Top by rankedPlayCount", "#"*15)
#for rank, stats in enumerate(pcount_rank):
#    if rank < 10:
#        print(" {:>2} - {:>30}     (ranked_count: {}  ranked_accu: {:.2f})".format(rank+1, stats[0], stats[1][0], stats[1][1]))

#print("#"*15, "Top by Accuracy", "#"*15)
if disc:
    output = "```"
    for rank, stats in enumerate(accu_rank):
        if rank < 15:
            name_p = stats[0]
            if len(stats[0]) > 22:
                name_p = stats[0][:22]
            output += "{:>2} - {:>23} (ranked_accu: {:.2f}  ranked_count: {})\n".format(rank+1, name_p, stats[1][1], stats[1][0])
    output += "```"
    print(output)
else:
    for rank, stats in enumerate(accu_rank):
        if rank < 15:
            print(" {:>2} - {:>30}     (ranked_accu: {:.2f}  ranked_count: {})".format(rank+1, stats[0], stats[1][1], stats[1][0]))
