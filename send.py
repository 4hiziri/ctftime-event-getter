import os
import mailer

def main():
    mailer.send('', configfile=os.path.expanduser('~/.notifier.conf'))

if __name__ == '__main__':
    main()
