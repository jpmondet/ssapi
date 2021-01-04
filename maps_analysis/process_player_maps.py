#! /usr/bin/env python3

import json
import pprint
from collections import defaultdict
from argparse import ArgumentParser

def handle_arguments():
    parser = ArgumentParser(
    prog="process_maps_player",
    description="Process the maps retrieved with all_maps_player.py",
    )
    parser.add_argument(
        "-p",
        "--player",
        type=str,
        help="Specify the ss id of the player. Exple : 76561198415354041",
    )
    args = parser.parse_args()
    
    return args
    
def main():

    args = handle_arguments()

    maps_playah = []
    with open(f'/root/ssapi/maps_analysis/all_maps_players_{args.player}.json', 'r') as fmaps:
        maps_playah = json.load(fmaps)

    scores = defaultdict(int)
    rankz = defaultdict(int)
    maps_scores = defaultdict(list)

    sum_average = 0.0
    ranked_maps = 0
    for mapp in maps_playah:
        #if mapp['maxScore'] == 0:
        #    print(mapp)
        #    continue
        if mapp['pp'] == 0:
            continue
        percent = int(mapp['score']) / int(mapp['maxScore']) * 100
        sum_average += percent
        ranked_maps += 1
        if percent < 90:
            maps_scores[percent].append(mapp)
            #print(mapp['songName'])
            #percent = 90
            scores[89] +=1
            continue
        scores[int(percent)] += 1
        rankz[mapp['rank']] += 1


    nb_maps =  len(maps_playah)
    scores_sorted = sorted(scores, reverse=True)
    print(f"\nTotal nb of maps = {nb_maps}")
    print(f"Total nb of ranked maps = {ranked_maps}")
    print(f"Average Acc on ranked = {sum_average / ranked_maps}")
    print("Details on ranked:")
    for scorz in scores_sorted:
        if scorz < 90:
            print(f"    Under 90 = {scores[scorz]}")
            continue
        print(f"    {scorz}+ = {scores[scorz]}")

    
    nb_worst_maps = 5
    print(f"\n{str(nb_worst_maps)} worst runs :")
    index = 1
    for scorz in sorted(maps_scores):
        for mapz in maps_scores[scorz]:
            if index >= (ranked_maps - nb_worst_maps);
                #print(f"{scorz:.2f} : {mapz['songName']:<50} ({mapz['difficultyRaw']}) set on {mapz['timeSet']}")
                print(f"{scorz:.2f} : {mapz['songName']:<20} (set on {mapz['timeSet']})")
            index += 1

    print("\nNumber of time in 'Tops' on ranked maps:")
    rankz_sorted = sorted(rankz, reverse=True)
    top3z = 0
    top5z = 0
    top10z = 0
    top25z = 0
    top50z = 0
    top100z = 0
    for rank in rankz_sorted:
        #print(f"    {rank} = {rankz[rank]}")
        if rank <= 100:
            top100z += rankz[rank]
            if rank <= 50:
                top50z += rankz[rank]
                if rank <= 25:
                    top25z += rankz[rank]
                    if rank <= 10:
                        top10z += rankz[rank]
                        if rank <= 5:
                            top5z += rankz[rank]
                            if rank <= 3:
                                top3z += rankz[rank]
    print(f"top1:   {rankz[1]} times, \n\
top3:   {top3z} times, \n\
top5:   {top5z} times, \n\
top10:  {top10z} times, \n\
top25:  {top25z} times, \n\
top50:  {top50z} times, \n\
top100: {top100z} times")

if __name__ == "__main__":
    main()
