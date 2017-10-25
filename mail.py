import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

smtp_server = sys.argv[1]
from_address = 'my-ctftime-daemon'
to_address = sys.argv[2]
charset = 'UTF-8'
subject = 'Next CTF!!'
text = sys.argv[1]
msg = MIMEText(text.encode(charset), 'plain', charset)

msg['Subject'] = Header(subject, charset)
msg['From'] = from_address
msg['To'] = to_address
msg['Date'] = formatdate(localtime=True)

smtp = smtplib.SMTP(smtp_server)
smtp.sendmail(from_address, to_address, msg.as_string())

smtp.close()
