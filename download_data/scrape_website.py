import urllib2
import re
import BeautifulSoup

site =  'http://www.gapminder.org/data/'
hdr = {
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Connection': 'keep-alive',
	'User-Agent' : 'Mozilla/5.0'}

req = urllib2.Request(site, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

print page
html = page.read()
print html


html = BeautifulSoup(page)
table = html.find('table', 't1')
links = table.findAll('a')
print links

url = 'http://www.gapminder.org/data/' 
#url = 'http://www.google.com'
#connect to a URL
website = urllib2.urlopen(url)

print website
#read html code
html = website.read()

#use re.findall to get all the links
links = re.findall('"((spreadsheets|google)s?://.*?)"', html)

print links
