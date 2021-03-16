#Test app for flask, may have to copy to BracketMaker
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

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






@app.route('/')
def index():
    full_df = pd.read_csv('/Users/etiennecossart/Desktop/CodingStuff/PythonProjects/MarchMadness/TeamScoreCalculator/Resources/2019full.csv', header=0, dtype=schemaDict)
    return full_df.to_html()

@app.route('/<name>')
def print_name(name):
    return 'Hi, {}'.format(name)