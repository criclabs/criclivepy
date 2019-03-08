from urllib.request import Request, urlopen
import sys, time
from bs4 import BeautifulSoup
import re

root_url = "https://m.cricbuzz.com/live-cricket-scorecard"

def sanitize(name):
    name = name.replace('(c)', '')
    return name.replace('(wk)', '')

def get_batting_scores(batting_div):
    print()
    print('Batting:')
    tables = batting_div.find_all("table", class_="table table-condensed")
    for idt, table in enumerate(tables):
        if idt==0:#Heading table
            continue
        rows = table.find_all("tr")
        for idr, row in enumerate(rows):
            if idr%2==0:
                j = {}
                cols = row.find_all("td")
                name = cols[0].get_text()
                # profile = cols[0].find_all("a")[0]['href']
                r_b = re.split('\(|\)', cols[1].get_text())
                fours = cols[2].get_text()
                sixes = cols[3].get_text()
                # s_r = cols[4].get_text()
                j['name'] = sanitize(name)
                # j['profile'] = profile
                j['runs'] = int(r_b[0])
                j['balls'] = int(r_b[1])
                j['fours'] = int(fours)
                j['sixes'] = int(sixes)
                # j['s_r'] = 100*int(r_b[0])/int(r_b[1])
                print(j)

def get_bowling_scores(bowling_div):
    print()
    print('Bowling:')
    tables = bowling_div.find_all("table", class_="table table-condensed")
    for idt, table in enumerate(tables):
        rows = table.find_all("tr")
        for idr, row in enumerate(rows):
            if idr==0:#Bowler Subheading row
                continue
            j = {}
            cols = row.find_all("td")
            name = cols[0].get_text()
            overs = cols[1].get_text()
            maiden = cols[2].get_text()
            runs = cols[3].get_text()
            wicket = cols[4].get_text()
            j['name'] = sanitize(name)
            j['overs'] = int(overs)
            j['maiden'] = int(maiden)
            j['runs'] = int(runs)
            j['wicket'] = int(wicket)
            print(j)

def get_fow_scores(fow_div):
    print()
    print('Fall of Wickets:')
    tables = fow_div.find_all("table", class_="table table-condensed")
    for idt, table in enumerate(tables):
        # if idt==0:#Heading table
        #     continue
        rows = table.find_all("tr")
        for idr, row in enumerate(rows):
            if idr==0:#Bowler Subheading row
                continue
            j = {}
            cols = row.find_all("td")
            wkt = cols[0].get_text()
            runs = cols[1].get_text()
            ovr = cols[2].get_text()
            batsman = cols[3].get_text()
            j['wkt'] = int(wkt)
            j['runs'] = int(runs)
            j['ovr'] = float(ovr)
            j['batsman'] = batsman
            print(j)

def get_match_scores(match_id, match_name, innings):
    req = Request(root_url +  "/" + match_id + "/" + match_name  + "/" + innings, headers={'User-Agent': 'Mozilla/5.0'})
    html_source = urlopen(req).read()
    parsed_html = BeautifulSoup(html_source, 'html.parser')

    table_divs = parsed_html.find_all("div", class_="table-row")
    batting_div = table_divs[0]
    bowling_div = table_divs[1]
    fow_div = table_divs[2]

    get_batting_scores(batting_div)
    get_bowling_scores(bowling_div)
    get_fow_scores(fow_div)

get_match_scores(match_id = "20794", match_name = "nz-vs-ban-1st-test-bangladesh-tour-of-new-zealand-2019", innings="1")


