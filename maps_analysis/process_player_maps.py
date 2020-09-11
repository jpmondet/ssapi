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
    with open(f'all_maps_players_{args.player}.json', 'r') as fmaps:
        maps_playah = json.load(fmaps)

    scores = defaultdict(int)
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
            #scores[89] +=1
            #continue
        scores[int(percent)] += 1


    nb_maps =  len(maps_playah)
    scores_sorted = sorted(scores, reverse=True)
    print(f"\nTotal nb of maps = {nb_maps}")
    print(f"Total nb of ranked maps = {ranked_maps}")
    print(f"Average on ranked = {sum_average / ranked_maps}")
    print("Details:")
    for scorz in scores_sorted:
        #if scorz == 89:
        #    print(f"    Under 90 :cry: = {scores[scorz]}")
        #else:
        print(f"    {scorz}+ = {scores[scorz]}")

    
    for scorz in sorted(maps_scores):
        for mapz in maps_scores[scorz]:
            print(f"{scorz:.2f} : {mapz['songName']:<50} ({mapz['difficultyRaw']}) set on {mapz['timeSet']}")

if __name__ == "__main__":
    main()
