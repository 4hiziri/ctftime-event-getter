import os
import mailer
from importlib import import_module


scraper_dir = 'scraper'


def get_scraper():
    dirs = os.listdir(scraper_dir)
    return [file[:-3] for file in dirs if file[-3:] == '.py']


def import_file(scraper_name):
    return import_module(scraper_dir + '.' + scraper_name)


def exec_scraper(scraper):
    try:
        text = import_file(scraper).fetch()
    except AttributeError as e:
        text = str(e)
        text += 'Scraper must has fetch() method.\n'

    return text


def main():
    for s in get_scraper():
        exec_scraper(s)
        mailer.send('', os.path.expanduser('notifier.conf'))

        


if __name__ == '__main__':
    main()

try:
    import_file('ctftime').fetch()
except AttributeError as e:
    print(e.traceback)
