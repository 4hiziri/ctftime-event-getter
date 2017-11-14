from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import urljoin

ctftime = 'https://ctftime.org/api/v1/'


def fetch_event_info(limit):
    path = ctftime + 'events/'
    payload = {'limit': limit}

    return requests.get(path, params=payload)


def get_title(json):
    return 'タイトル: ' + json['title']


def get_url(json):
    return json['url']


def get_start(json):
    def time_jpn(time_str):
        [h, m, s] = time_str.split(':')
        h = '{:02}'.format(int(h) + 9)
        return ':'.join([h, m ,s])

    time = json['start']
    [data, utc_time] = time.split('T')
    utc_time = utc_time.split('+')[0]
    japan_time = time_jpn(utc_time)
    return '開始時間: ' + data + " " + japan_time


def get_duration(json):
    fmt = ''
    fmt += '期間: '
    fmt += str(json['duration']['days']) + '日 '
    fmt += str(json['duration']['hours']) + '時間'
    return fmt


def get_format(json):
    return '形式: ' + json['format']


def get_place(json):
    place = '場所: '
    if json['onsite']:
        return place + json['location']
    else:
        return place + 'Online'


def get_description(json):
    ident = '-------------\n'
    return ident + json['description'] + '\n' + ident


def format_json(json):
    fmt = ''

    fmt += get_title(json) + '\n'
    fmt += get_url(json) + '\n'
    fmt += get_start(json) + '\n'
    fmt += get_duration(json) + '\n'
    fmt += get_format(json) + '\n'
    fmt += get_place(json) + '\n'
    fmt += get_description(json) + '\n'

    return fmt


def scrape():
    fmt = ''
    part = '=============================\n'

    for json in fetch_event_info(5).json():
        fmt += part
        fmt += format_json(json) + '\n'
        fmt += part

    return fmt


def main():
    for json in fetch_event_info(5).json():
        print(format_json(json))
    return


if __name__ == '__main__':
    main()
