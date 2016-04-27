# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--cmd',help='if provide, the command will be execute and the output will be logged to the log file')
parser.add_argument('--log',help='the log file that will be sent to the mail')

args=parser.parse_args()

print args.cmd

# exit(0)



textfile = 'sendmail.py'



conf_file=open('email.conf','r')
smtp_url=conf_file.readline().strip('\n').strip()
add_from=conf_file.readline().strip('\n').strip()
add_from_pass=conf_file.readline().strip('\n').strip()
add_to=conf_file.readline().strip('\n').strip()
conf_file.close()

message = MIMEMultipart()

message['Subject'] = Header('The contents of %s' % textfile, 'utf-8')
message['From'] = Header(add_from, 'utf-8')
message['To'] = Header(add_to, 'utf-8')


msg = MIMEText('assdddddddddddd', 'plain', 'utf-8')
message.attach(msg)

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open(textfile, 'rb')
# Create a text/plain message
att1 = MIMEText(fp.read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename="test.txt"'

fp.close()

message.attach(att1)


# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP_SSL(smtp_url)
s.login(add_from, add_from_pass)
s.sendmail(add_from, [add_to], message.as_string())
s.quit()
