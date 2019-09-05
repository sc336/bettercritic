from bs4 import BeautifulSoup
import urllib2

def soup_from_url(url):
    req = urllib2.Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
    conn = urllib2.urlopen(req)
    html = conn.read()
    return BeautifulSoup(html)
