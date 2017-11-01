from configparser import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate


class Mailer:
    def __init__(self, addr, passcode):
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.addr = addr
        self.passcode = passcode
        self.charset = 'UTF-8'

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
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.ehlo()
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
    conf = readConfig(configfile)

    mailer = Mailer(conf['addr'], conf['pass'])
    mailer.setCharset(conf['charset'])
    mailer.send(conf['to'], conf['from'], subject, text)
    mailer.close()


if __name__ == '__main__':
    import sys

    subject = sys.argv[1]
    text = sys.argv[2]

    send(subject, text, 'config.conf')
