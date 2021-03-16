from ast import Num
from os import WIFSIGNALED
import sys
import fileinput
import csv
import numpy as np
from numpy.lib.function_base import append
import pandas as pd


pd.set_option('display.max_rows', None)
print(" - - 1010 Productions - - -")
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
team_score_lookup = {}
champFinal = []
winnersCircle = []
losersCircle = []
w_names=[]
l_names=[]
finFour=[]

full_df = pd.read_csv('/Users/etiennecossart/Desktop/CodingStuff/PythonProjects/MMBracketMaker/TeamScoreCalculator/Resources/2021_data.csv', header=0, dtype=schemaDict)
print(full_df)


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

    a_wate = input("What is your [AdjEM] Weight?   :    ")
    b_wate = input("What is your [AdjO] Weight?   :    ")
    c_wate = input("What is your [AdjD] Weight?   :    ")
    d_wate = input("What is your [AdjT] Weight?   :    ")
    e_wate = input("What is your [Luck] Weight?   :    ")
    f_wate = input("What is your [SchAdjEM] Weight?   :    ")
    g_wate = input("What is your [SchOppO] Weight?   :    ")
    h_wate = input("What is your [SchOppD] Weight?   :    ")
    i_wate = input("What is your [NonConfSchAdjEM] Weight?   :    ")

    a = float(a_wate)
    b = float(b_wate)
    c = float(c_wate)
    d = float(d_wate)
    e = float(e_wate)
    f = float(f_wate)
    g = float(g_wate)
    h = float(h_wate)
    i = float(i_wate)
    print(a, b, c, d, e, f, g, h, i)
    full_df['AdjEM'] = a * full_df['AdjEM']

    full_df['AdjO'] = b * full_df['AdjO']

    full_df['AdjD'] = c * full_df['AdjD']

    full_df['AdjT'] = d * full_df['AdjT']

    full_df['Luck'] = e * full_df['Luck']

    full_df['SchAdjEM'] = f * full_df['SchAdjEM']

    full_df['SchOppO'] = g * full_df['SchOppO']

    full_df['SchOppD'] = h * full_df['SchOppD']
    
    full_df['NonConfSchAdjEM'] = i * full_df['NonConfSchAdjEM']

    comp_score = full_df['AdjEM'] + full_df['AdjO'] + full_df['AdjD'] + full_df['AdjT'] + full_df['Luck'] + \
    full_df['SchAdjEM'] + full_df['SchOppO'] + \
    full_df['SchOppD'] + full_df['NonConfSchAdjEM']

    full_df['COMPOSITE_SCORE'] = comp_score
    sortded_composite_df = full_df.sort_values(by=['COMPOSITE_SCORE'])
    print(sortded_composite_df)


# TODO: once function is updated, uncomment
# scalar_time()
# TODO: fault tolerance for tight games, rand num for percent of UPSETS

scalar_time()
# print(sortded_composite_df)
# print("##############################################################")
# valid = False
# while valid == False:
#     confirm = input("Does it look good? ^^ (y/n)")
#     if confirm == "y":
#         print("CONFIRMED!")
#         print("Calculating......")
#         valid = True
#     elif confirm == "n":
#         scalar_time()
#     else:
#         print(" INVALID ENTRY: ", str(confirm), " Required: (y/n)")


matchup = []
for region in regionPosition:
    for seed_rank in seedPosition:
        # print("~~~~~~~~")
        # print(str(region), str(seed_rank))
        team_index = int(full_df[(full_df['REGION'] == region) & (full_df['SEED'] == seed_rank)].index[0])
        team_score = float(full_df[['COMPOSITE_SCORE']].loc[(full_df['REGION'] == region) & (full_df['SEED'] == seed_rank)].values)
        matchup.append(team_index)
        team_score_lookup[team_index] = team_score

        # print(matchup)
        # print(team_score_lookup)
        # print("-------")



numTeamsRem = len(matchup)

while(numTeamsRem % 2 == 0):
    winnersCircle.clear()
    losersCircle.clear()
    w_names.clear()
    l_names.clear()
    it_matchups = iter(matchup)
    counter = 0
    for team_ind in it_matchups:
        counter += 1
        a_int = team_ind
        b_int = next(it_matchups)

        a_team_name = full_df._get_value(int(a_int), 'TEAM')
        b_team_name = full_df._get_value(int(b_int), 'TEAM')
        a_team_score = team_score_lookup[a_int]
        b_team_score = team_score_lookup[b_int]

        a_team_region = full_df._get_value(int(a_int), 'REGION')
        b_team_region = full_df._get_value(int(b_int), 'REGION')
        a_team_seed = full_df._get_value(int(a_int), 'SEED')
        b_team_seed = full_df._get_value(int(b_int), 'SEED')

        print(" ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ Match Up ~ ", str(counter) ," ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
        print (str(a_team_name), str(a_int), " | ", str(a_team_score), " | ", str(a_team_region), " | ", str(a_team_seed))
        print (str(b_team_name), str(b_int), " | ", str(b_team_score), " | ", str(b_team_region), " | ", str(b_team_seed))
        print("")

        if a_team_score > b_team_score:
            winnersCircle.append(a_int)
            w_names.append(a_team_name)
            losersCircle.append(b_int)
            l_names.append(b_team_name)
        elif a_team_score == b_team_score:
            if a_int > b_int:
                winnersCircle.append(a_int)
                w_names.append(a_team_name)
                losersCircle.append(b_int)
                l_names.append(b_team_name)
        else:
            winnersCircle.append(b_int)
            w_names.append(b_team_name)
            losersCircle.append(a_int)
            l_names.append(a_team_name)   
    matchup.clear() 
    matchup = winnersCircle.copy()
    numTeamsRem = len(matchup)
    print_string = "#"
    print_string_len = print_string + " Round of " + str(numTeamsRem) + ": "+ str(w_names) + " " + print_string
    string_len = len(print_string_len)
    print("")
    print(print_string*string_len)
    print (print_string_len)
    print(print_string*string_len)
    print()




