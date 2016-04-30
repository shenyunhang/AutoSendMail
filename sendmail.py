# -*-coding:utf-8-*-
import os
import argparse
import ConfigParser
import subprocess

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

#---------------------------------------------------------------
# 参数处理
parser = argparse.ArgumentParser()

parser.add_argument('-c', '--cmd', metavar='command', type=str,
                    help='if provide, the command will be execute and the output will be logged to the log file')
parser.add_argument('-l', '--log', metavar='log_path', type=str,
                    help='the log file that will be sent to the mail')
args = parser.parse_args()

if not (args.log or args.cmd):
    parser.error('at least one of --log and --cmd required"')

log_path = None
command = None


if args.log is not None and args.cmd is not None:
    print args.log
    print args.cmd
    log_path = args.log
    command = '{} |tee {}'.format(args.cmd, log_path)
    subprocess.call(command, shell=True)
elif args.log is not None:
    log_path = args.log
    if not (os.path.exists(log_path) and os.path.isfile(log_path)):
        print 'log file %s not found' % log_path
else:
    log_path = 'log.log'
    command = '{} |tee {}'.format(args.cmd, log_path)
    subprocess.call(command, shell=True)


if args.cmd is not None:
    print args.cmd
    command = '{} |tee'.format(args.cmd)
    subprocess.call(command, shell=True)

#---------------------------------------------------------------
# 读取配置文件
conf_name = 'email.conf'
self_file_dir = os.path.split(os.path.realpath(__file__))[0]
# self_file_path = os.path.realpath(__file__)
conf_path = os.path.join(self_file_dir, conf_name)

config_sec = ['send', 'receive']
config_op = ['smtp_url', 'send_address', 'send_password', 'receive_address']

config = ConfigParser.ConfigParser()
config.read(conf_path)
if not (config.has_section(config_sec[0]) and config.has_section(config_sec[1])):
    exit(0)

if not config.has_option(config_sec[0], config_op[0]):
    print 'no %s', config_op[0]
    exit(0)
smtp_url = config.get(config_sec[0], config_op[0])

if not config.has_option(config_sec[0], config_op[1]):
    print 'no %s', config_op[1]
    exit(0)
add_from = config.get(config_sec[0], config_op[1])


if not config.has_option(config_sec[0], config_op[2]):
    print 'no %s', config_op[2]
    exit(0)
add_from_pass = config.get(config_sec[0], config_op[2])

if not config.has_option(config_sec[1], config_op[3]):
    print 'no %s', config_op[3]
    exit(0)
add_to = config.get(config_sec[1], config_op[3])

# conf_file = open(conf_path, 'r')
# smtp_url = conf_file.readline().strip('\n').strip()
# add_from = conf_file.readline().strip('\n').strip()
# add_from_pass = conf_file.readline().strip('\n').strip()
# add_to = conf_file.readline().strip('\n').strip()
# conf_file.close()

#---------------------------------------------------------------
# 初始化邮件
message = MIMEMultipart()

message['Subject'] = Header('The contents of %s' % log_path, 'utf-8')
message['From'] = Header(add_from, 'utf-8')
message['To'] = Header(add_to, 'utf-8')

msg = MIMEText('assdddddddddddd', 'plain', 'utf-8')
message.attach(msg)

#---------------------------------------------------------------
# 读取log文件
# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open(log_path, 'rb')
# Create a text/plain message
att1 = MIMEText(fp.read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename="test.txt"'
fp.close()

message.attach(att1)

#---------------------------------------------------------------
# 发送邮件
# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP_SSL(smtp_url)
s.login(add_from, add_from_pass)
s.sendmail(add_from, [add_to], message.as_string())
s.quit()
