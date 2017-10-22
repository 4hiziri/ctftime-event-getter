from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urljoin

ctftime = 'https://ctftime.org/api/v1/'


def fetch_event_info(limit):
    path = ctftime + 'events/'
    payload = {'limit': limit}

    return requests.get(path, params=payload)


def format_json(json):
    fmt = ''
    fmt += json['title']
    fmt += '(' + json['url'] + ')'
    fmt += '\n'
    fmt += json['start']

    return fmt


def main():
    for json in fetch_event_info(4).json():
        print(format_json(json))
        print('\n\n')
    return


if __name__ == '__main__':
    main()
