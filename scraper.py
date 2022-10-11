#Web scraper. Checks a website and finds broken links.
import requests
from bs4 import BeautifulSoup
from http.client import responses
import argparse
import re
import sys

def removeDup(numList):
    test = []
    for x in numList:
        if x not in test:
            test.append(x)
 
    return test

def help():
    print('''
Scraper - Collect links from specified page and verify status

usage: 
        python3 scraper.py -u/--url https://evilcorp.com
    
    ''')

    sys.exit(0)

def collect_links(url):
    try:
        html = requests.get(url)
        
    except:
        print("Unable to perform request against '{}'\n".format(url))
        help()

    pages = html.content
    
    soup = BeautifulSoup(pages, 'html.parser')
    
    links = []
 
    for link in soup.find_all('a'):
        links.append(link.get('href'))
 
    return links

def get_codes(links):
    print('-' * 60)
    clean_print("STATUS", "MESSAGE", "LINK")
    print('-' * 60)
    for link in links:
        try:
            testpage = requests.get(link)
        except:
            continue
        status = testpage.status_code

        linktest = ''

        if status == 404:
            #print(str(link) + ": Broken")
            #clean_print("BROKEN", link)
            linktest = 'BROKEN'
    
        elif status == 200:
            #print(str(link) + ": Good")
            #clean_print("GOOD", link)
            linktest = 'GOOD'
        
        else:
            linktest = 'UNKNOWN'

        message = resolve_code(status)

        clean_print(linktest, message, link)

    print('-' * 60)


def resolve_code(status):
    try:
        return responses[status]

    except:
        return 'Unresolved: {}'.format(status)

def clean_print(status, message, link):
    print('{0: <10}| {1: <20}| {2}'.format(status, message, link))

def main():

    parser = argparse.ArgumentParser(description='Accept a website to scrape')
    parser.add_argument('-u','--url', dest='target_url', required=True, help='URL to scrape for links')

    args = parser.parse_args()

    if not re.match('^http(s)://\S+$', args.target_url):
        args.target_url = 'https://' + args.target_url
        #help()

    raw_links = collect_links(args.target_url)
    refined_links = removeDup(raw_links)

    get_codes(refined_links)

if __name__ == '__main__':
    main()
