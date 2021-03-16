from ast import Num
from os import WIFSIGNALED
import sys
import fileinput
import csv
import numpy
from numpy.lib.function_base import append
import pandas as pd

print("is this wokring?!?!?!?")
schemaDict = {
    'TEAM': str,
    'REGION': str,
    'SEED': int,
    'AdjEM': float,
    'AdjO': float,
    'AdjD': float,
    'AdjT': float,
    'Luck': float,
    'SchAdjEM': float,
    'SchAdjO': float,
    'SchAdjD': float,
    'NonConfSchAdjEM': float,
}

regionPosition = ['E', 'W', 'S', 'M']  # make dictionary for full region
seedPosition = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
final_four={
    regionPosition[0] : "",
    regionPosition[1] : "",
    regionPosition[2] : "",
    regionPosition[3] : ""
}
champFinal = []
winnersCircle = []
losersCircle = []
w_names=[]
l_names=[]
finFour=[]

full_df = pd.read_csv('/Users/etiennecossart/Desktop/CodingStuff/PythonProjects/MarchMadness/TeamScoreCalculator/Resources/2019full.csv', header=0, dtype=schemaDict)


# Inputs/Wates/etc.
# TODO: update for full data set, proper vars, etc. DONT CALL TILL THEN
def scalar_time():
    a_wate = ""
    b_wate = ""
    c_wate = ""
    d_wate = ""
    e_wate = ""
    f_wate = ""
    g_wate = ""
    h_wate = ""

    a_wate = input("What is your A Weight?   :    ")
    b_wate = input("What is your B Weight?   :    ")
    c_wate = input("What is your C Weight?   :    ")
    d_wate = input("What is your D Weight?   :    ")
    e_wate = input("What is your E Weight?   :    ")
    f_wate = input("What is your F Weight?   :    ")
    g_wate = input("What is your G Weight?   :    ")
    h_wate = input("What is your H Weight?   :    ")

    a = float(a_wate)
    b = float(b_wate)
    c = float(c_wate)
    d = float(d_wate)
    e = float(e_wate)
    f = float(f_wate)
    g = float(g_wate)
    h = float(h_wate)
    print(a, b, c, d, e, f, g, h)
    full_df['A'] = full_df['A'].astype(float)
    full_df['A'] = a * full_df['A']

    full_df['B'] = full_df['B'].astype(float)
    full_df['B'] = b * full_df['B']

    full_df['C'] = full_df['C'].astype(float)
    full_df['C'] = c * full_df['C']

    full_df['D'] = full_df['D'].astype(float)
    full_df['D'] = d * full_df['D']

    full_df['E'] = full_df['E'].astype(float)
    full_df['E'] = e * full_df['E']

    full_df['F'] = full_df['F'].astype(float)
    full_df['F'] = f * full_df['F']

    full_df['G'] = full_df['G'].astype(float)
    full_df['G'] = g * full_df['G']

    full_df['H'] = full_df['H'].astype(float)
    full_df['H'] = h * full_df['H']
    print(h * full_df['H'])

# TODO: once function is updated, uncomment
# scalar_time()
# TODO: fault tolerance for tight games, rand num for percent of UPSETS


comp_score = full_df['AdjEM'] + full_df['AdjO'] + full_df['AdjD'] + full_df['AdjT'] + full_df['Luck'] + \
    full_df['SchAdjEM'] + full_df['SchOppO'] + \
    full_df['SchOppD'] + full_df['NonConfSchAdjEM']
full_df['COMPOSITE_SCORE'] = comp_score
sortded_composite_df = full_df.sort_values(by=['COMPOSITE_SCORE'])
# print(sortded_composite_df)
print("##############################################################")


# Function that takes in the seed list, compares teams in seed list by match up, adds winners to
def roundMatchUps(seeds):
    print("Seeds to process: ", str(seeds))
    it_seeds = iter(seeds)
    for seed_rank in it_seeds:
        a_seed = seed_rank
        b_seed = next(it_seeds)
        print("####matchup:: ", str(a_seed), str(b_seed))
        a_team_name = str(full_df[['TEAM']].loc[(
            full_df['REGION'] == region) & (full_df['SEED'] == a_seed)].values)
        b_team_name = str(full_df[['TEAM']].loc[(
            full_df['REGION'] == region) & (full_df['SEED'] == b_seed)].values)
        a_team_score = float(full_df[['COMPOSITE_SCORE']].loc[(
            full_df['REGION'] == region) & (full_df['SEED'] == a_seed)].values)
        b_team_score = float(full_df[['COMPOSITE_SCORE']].loc[(
            full_df['REGION'] == region) & (full_df['SEED'] == b_seed)].values)
        print("team A:", str(a_team_name), str(a_team_score), str(a_seed))
        print("team B:", str(b_team_name), str(b_team_score), str(b_seed))

        if a_team_score > b_team_score:
            winnersCircle.append(a_seed)
            w_names.append(a_team_name)
            losersCircle.append(b_seed)
            l_names.append(b_team_name)
        elif a_team_score == b_team_score:
            if a_seed > b_seed:
                winnersCircle.append(a_seed)
                w_names.append(a_team_name)
                losersCircle.append(b_seed)
                l_names.append(b_team_name)
        else:
            winnersCircle.append(b_seed)
            w_names.append(b_team_name)
            losersCircle.append(a_seed)
            l_names.append(a_team_name)

        print("LOSERS CIRCLE:", str(losersCircle))
        print("Winners CIRCLE:", str(winnersCircle)) 
        print("Winners:", str(w_names))
        print("Losers:", str(l_names))

    for loser in losersCircle:
        # TODO: if catch for if loser NOT in seeds, fail
        print("REMOVING LOSER", str(loser))
        seeds.remove(loser)

    print("")
    return seeds


# def compare():
    # For earch region in the list, going in order.
    # 1) set seeds[] to OG list
    # 2) find numTeamsRemaining by  seeds / 2
    # 3) While loop of numTeamsRem of if mod 2 % 0
    # 4) for loop of every 2 in seeds (1st, second)
    # 5) set a-team, b-Team names/scores
    # 6) 3 ifs: if a>b -> a append winnerCircle[], a=b {nest if aSeed > bSeed} -> a append winnerCircle[], else: b append winnerCircle[]
    # 7) set seeds = winners circle
    # 8) end of Seedds for loop, reset seeds
    
for region in regionPosition:
    print("PROCESSING:   ", str(region))
    seeds = seedPosition.copy()
    numTeamsRem = len(seeds)  # TODO move it as last action for the round

    # Doing all the larger brackets until Division Champ
    while (numTeamsRem % 2 == 0):
        winnersCircle.clear()
        losersCircle.clear()
        w_names.clear()
        l_names.clear()
        roundMatchUps(seeds)
        seeds.clear()
        seeds = winnersCircle.copy()
        numTeamsRem = len(seeds)
        print(numTeamsRem)
    final_four[region] = winnersCircle[0]
    print(final_four)
    # finalFour.append(winnersCircle)
    # finFour.append(w_names)

best_four = full_df.sort_values(by=['COMPOSITE_SCORE'])
print(best_four)


div_champs = iter(regionPosition)
for team in div_champs:
    a_finals_seed = final_four.get(team)
    b_finals_seed = final_four.get(next(div_champs))
    print(str(a_finals_seed))
    print(str(b_finals_seed))



