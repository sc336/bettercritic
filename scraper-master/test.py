from bs4 import BeautifulSoup
import urllib2
import sys

vgchartz_page = 1

vgchartz_url = "http://www.vgchartz.com/gamedb/?page=" + str(vgchartz_page) + "&results=1000&name=&platform=&minSales=0&publisher=&genre=&sort=GL"
#vgchartz_url = "file:vgchartz.htm"	# This is a DEBUG line - pulling vgchartz data from filesystem. Comment it out for production.
vgchartz_conn = urllib2.urlopen(vgchartz_url)
vgchartz_html = vgchartz_conn.read()
sys.stdout.write("connected.\n")

vgsoup = BeautifulSoup(vgchartz_html)
rows = vgsoup.find(string='Wii sports')
print r.parent
# print vgsoup.find('tr')
