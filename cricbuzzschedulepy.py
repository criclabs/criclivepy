from urllib.request import Request, urlopen
import sys, time
from bs4 import BeautifulSoup
import re
import pprint as pp

root_url = "https://www.cricbuzz.com"
schedule = "cricket-schedule"
upcoming = 'upcoming-series'
types = ['international', 'domestic', 'league', 'women']

def sanitize(name):
    name = name.replace(' - Live Cricket Score, Commentary', '')
    return name

def get_match(url):
    req = Request(root_url + url)
    html_source = urlopen(req).read()
    parsed_html = BeautifulSoup(html_source, 'html.parser')

    j = {}

    header = parsed_html.find("h1",  {"itemprop" : "name"})
    try:
        j['title'] = sanitize(header.get_text())
    except Exception as e:
        print(e)

    date_span = parsed_html.find("span",  {"itemprop" : "startDate"})
    try:
        date_val = date_span['content']
        j['date_val'] = date_val
    except Exception as e:
        print(e)

    pp.pprint(j)

for _type in types:
    req = Request(root_url +  "/" +  schedule + "/" + upcoming + "/" + _type)
    html_source = urlopen(req).read()
    parsed_html = BeautifulSoup(html_source, 'html.parser')

    a_s = parsed_html.find_all("a")
    for a in a_s:
        try:
            ahref = a['href']
            if 'live-cricket-scores' in ahref:
                get_match(ahref)
        except Exception as e:
            pass
    print()



