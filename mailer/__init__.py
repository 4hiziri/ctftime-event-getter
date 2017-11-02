from configparser import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate
import ssl


class Mailer:
    def __init__(self, smtp, port, user, passcode, charset):
        try:
            self.smtp = smtplib.SMTP_SSL(smtp, port)            
        except ssl.SSLError as e:
            print(e)
            print('SSL/TLS failed, try STARTTLS.')
            self.smtp = smtplib.SMTP(smtp, port)
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo()

        self.addr = user
        self.passcode = passcode
        self.charset = charset

        return

    def setCharset(self, charset):
        self.charset = charset

    def getMsg(self, to_addr, from_addr, subject, text):
        msg = MIMEText(text.encode(self.charset),
                       'plain',
                       self.charset)
        msg['Subject'] = Header(subject, self.charset)
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Date'] = formatdate(localtime=True)

        return msg

    def send(self, to_addr, from_addr, subject, text):        
        self.smtp.login(self.addr, self.passcode)
        msg = self.getMsg(to_addr, from_addr, subject, text).as_string()
        self.smtp.sendmail(from_addr,
                           [to_addr],
                           msg)

    def close(self):
        self.smtp.close()


def readConfig(filename):
    config = ConfigParser()
    config.read(filename)

    default = {'from': 'my-mailer-bot',
               'charset': 'UTF-8',
               'subject': 'Mailer-Bot'}

    default.update(config['setting'])

    return default


def send(subject, text, configfile):
    import os
    if not os.path.exists(configfile):
        print('Configfile Not Found: ' + configfile)
        exit(1)
    conf = readConfig(configfile)
    mailer = Mailer(conf['smtp'], int(conf['port']),
                    conf['user'], conf['pass'], conf['charset'])
    mailer.setCharset(conf['charset'])
    mailer.send(conf['to'], conf['from'], subject, text)
    mailer.close()


if __name__ == '__main__':
    import sys

    subject = sys.argv[1]
    text = sys.argv[2]

    send(subject, text, 'mailer.conf')
