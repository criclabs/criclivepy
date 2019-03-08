from urllib.request import Request, urlopen
import sys, time
from bs4 import BeautifulSoup
import re
import pprint as pp

root_url = "https://www.espncricinfo.com"

def sanitize(name):
    name = name.replace('(c)', '')
    return name.replace('(wk)', '')

def get_batting_scores(batting_div):
    print()
    print('Batting:')
    rows = batting_div.find_all("div", class_="wrap batsmen")
    for row in rows:
        j = {}
        cols = row.find_all("div", class_="cell")
        name = cols[0].get_text()
        runs = cols[2].get_text()
        balls = cols[3].get_text()
        fours = cols[4].get_text()
        sixes = cols[5].get_text()
        s_r = cols[6].get_text()
        j['name'] = sanitize(name)
        j['runs'] = int(runs)
        j['balls'] = int(balls)
        j['fours'] = int(fours)
        j['sixes'] = int(sixes)
        j['s_r'] = 100*int(runs)/int(balls)
        print(j)

def get_bowling_scores(bowling_div):
    print()
    print('Bowling:')
    rows = bowling_div.find_all("tr", class_="")
    for row in rows:
        j = {}
        cols = row.find_all("td", class_="")
        if len(cols)<6:
            continue
        try:
            name = cols[0].find_all("a")[0].get_text()
            overs = cols[1].get_text()
            maidens = cols[2].get_text()
            runs = cols[3].get_text()
            wickets = cols[4].get_text()
            econ = cols[5].get_text()
            j['name'] = sanitize(name)
            j['overs'] = int(overs)
            j['maidens'] = float(maidens)
            j['runs'] = int(runs)
            j['wickets'] = float(wickets)
            j['econ'] = float(econ)
            print(j)
        except Exception as e:
            print(e)

def get_fow_scores(fow_div):
    print()
    print('Fall of Wickets:')
    fows = fow_div.get_text().split('),')
    for fow in fows:
        print(fow)

def get_match_scores(series_id, match_id, match_name):
    req = Request(root_url + '/series/' + series_id + "/scorecard/" + match_id + "/" + match_name, headers={'User-Agent': 'Mozilla/5.0'})
    html_source = urlopen(req).read()
    parsed_html = BeautifulSoup(html_source, 'html.parser')

    batting_divs = parsed_html.find_all("div", class_="scorecard-section batsmen")
    bowling_divs = parsed_html.find_all("div", class_="scorecard-section bowling")
    fow_divs = parsed_html.find_all("div", class_="wrap dnb")

    for inn in range(2):
        print()
        print("Innnings:", 1 + inn)
        try:
            get_batting_scores(batting_divs[inn])
        except Exception as e:
            print(e)

        try:
            get_bowling_scores(bowling_divs[inn])
        except Exception as e:
            print(e)

        try:
            get_fow_scores(fow_divs[inn])
        except Exception as e:
            print(e)

get_match_scores(series_id = "19117", match_id = "1172164", match_name = "india-women-vs-england-women-2nd-t20i-eng-w-in-india-2018-19")
get_match_scores(series_id = "19059", match_id = "1168243", match_name = "india-vs-australia-2nd-odi-aus-in-ind-2018-19")
