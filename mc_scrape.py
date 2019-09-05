import json
import codecs
from bs4 import BeautifulSoup
import urllib2
import datetime
import logging

logging.basicConfig(filename="log-" + datetime.datetime.now().strftime("%Y%m%d-%H_%M_%S") + ".txt", level=logging.DEBUG)

metacritic_platform = {'PS3': 'playstation-3',
                       'X360': 'xbox-360',
                       'PC': 'pc',
                       'WiiU': 'wii-u',
                       '3DS': '3ds',
                       'PSV': 'playstation-vita',
                       'iOS': 'ios',
                       'Wii': 'wii',
                       'DS': 'ds',
                       'PSP': 'psp',
                       'PS2': 'playstation-2',
                       'PS': 'playstation',
                       'XB': 'xbox', # original xbox
                       'GC': 'gamecube',
                       'GBA': 'game-boy-advance',
                       'DC': 'dreamcast',
                       'PS4': 'playstation-4',
                       'XOne': 'xbox-one'
                       }

def soup_from_url(url):
    req = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    try:
        logging.info('Connecting to ' + url)
        conn = urllib2.urlopen(req)
        html = conn.read()
        return BeautifulSoup(html)
    except Exception as e:
        logging.info(e)
        return None

def dict_source_from_soup(s):
    try:
        return { 'source' : s.find(class_='source').get_text(), 'score' : int(s.find(class_='review_grade').get_text())}
    except:
        logging.info('Failed to load source ' + s.find(class_='source').get_text())
        logging.debug(s)

vgc_data = json.loads(codecs.open('scraper-master/data-20190216-23_48_18.json', 'r', 'utf-8').read())

outfilename = "criticdata-" + datetime.datetime.now().strftime("%Y%m%d-%H_%M_%S") + ".json"

with open("log-" + datetime.datetime.now().strftime("%Y%m%d-%H_%M_%S") + ".txt", 'w') as log:
    with codecs.open(outfilename, 'w', 'utf-8') as f:
        f.write('[')
        for r in vgc_data:
            if r['platform'] in metacritic_platform:
                logging.info('Scraping ' + r['basename'])
                mc_url = 'https://www.metacritic.com/game/' + metacritic_platform[r['platform']] + '/' + r['basename']
                r['mc_url'] = mc_url
                soup = soup_from_url(mc_url)
                if soup is not None:
                    json_from_mc = json.loads(soup.find(type='application/ld+json').get_text())
                    source_soup = [ s.parent.parent for s in soup.find_all(class_='source')]
                    source_list = [dict_source_from_soup(s) for s in source_soup ]
                    json_from_mc['reviews'] = source_list
                    f.write(json.dumps(json_from_mc) + ',')
                    #TODO: remove final comma
                else:
                    logging.warning('Failed to connect')
        f.write(']')

