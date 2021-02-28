# Simple program to search magnet links in nyaa.si
# and copy them to your clipboard for easy download

import urllib.parse
import requests
import pyperclip
from bs4 import BeautifulSoup

# base url for searching
baseURL = 'https://nyaa.si/?f=0&c=0_0&q='

# get query as user input
query = input('Enter the search query: ')

print('Searching for "%s" in nyaa.si' % query)

# parse query into url safe string
urllib.parse.quote_plus(query, safe='/')

# get the result from the request
result = requests.get(baseURL + query)

print('Getting the magnet links...')

# extract the html from the result
src = result.content

# instantiate bs
soup = BeautifulSoup(src, 'lxml')

# find all rows with class success
rows = soup.find_all('tr', 'success')


# function to get title from column
def findTitle(tag):
    # title is a link with no class
    return tag.name == 'a' and not tag.has_attr('class')


titles = []
links = []

# loop through the rows and add the text and link to the dictionary
for row in rows:
    titles.append(row.find('td', attrs={"colspan": "2"}).find(findTitle).text)
    links.append(row.find('i', 'fa-magnet').parent['href'])

print("We've found % d items\n" % len(titles))

str = input('Would you like to check their names? (y/N): ').lower()

if(str == 'y' or str == 'yes' or str == 'ye'):
    print('These items found were:')
    for title in titles:
        print(title)


str = ''
for link in links:
    str += link + '\n'

pyperclip.copy(str)

print('The links have been copied to your clipboard. Enjoy!')

input('\nPress <Enter> to quit...')
