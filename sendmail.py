#!/usr/bin/python
# -*-coding:utf-8-*-
import os
import argparse
import ConfigParser
import subprocess
import time
from easydict import EasyDict as edict
import yaml

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

#---------------------------------------------------------------
# 参数处理
parser = argparse.ArgumentParser()

parser.add_argument(
    '-c',
    '--cmd',
    metavar='command',
    type=str,
    help=
    'if provide, the command will be execute and the output will be logged to the log file',
)
parser.add_argument(
    '-l',
    '--log',
    metavar='log_path',
    type=str,
    help='the log file that will be sent to the mail',
)
args = parser.parse_args()

if not (args.log or args.cmd):
    parser.error('at least one of --log and --cmd required"')

#---------------------------------------------------------------
# 读取配置文件
conf_name = 'email.yml'
self_file_dir = os.path.split(os.path.realpath(__file__))[0]
# self_file_path = os.path.realpath(__file__)
conf_path = os.path.join(self_file_dir, conf_name)

with open(conf_path, 'r') as f:
    yaml_cfg = edict(yaml.load(f))
print(yaml_cfg)
if 'send' not in yaml_cfg:
    print('configure file no send section!')
    exit()

if 'receive' not in yaml_cfg:
    print('configure file no receive section!')
    exit()

if 'smtp_url' not in yaml_cfg.send:
    print('configure file no smtp_url!')
    exit()

if 'send_address' not in yaml_cfg.send:
    print('configure file no send_address!')
    exit()

if 'send_password' not in yaml_cfg.send:
    print('configure file no send_password!')
    exit()

if 'receive_address' not in yaml_cfg.receive:
    print('configure file no receive_address!')
    exit()

smtp_url = yaml_cfg.send.smtp_url

add_from = yaml_cfg.send.send_address

add_from_pass = yaml_cfg.send.send_password

add_to = yaml_cfg.receive.receive_address

# conf_file = open(conf_path, 'r')
# smtp_url = conf_file.readline().strip('\n').strip()
# add_from = conf_file.readline().strip('\n').strip()
# add_from_pass = conf_file.readline().strip('\n').strip()
# add_to = conf_file.readline().strip('\n').strip()
# conf_file.close()

#---------------------------------------------------------------
log_path = args.log
if log_path is None:
    now = int(time.time())
    timeArray = time.localtime(now)
    # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    otherStyleTime = time.strftime("%Y%m%d%H%M%S", timeArray)
    log_path = '{}.log'.format(otherStyleTime)

cmd = args.cmd
if cmd is not None:
    # 执行命令
    cmd_execute = '{} |tee {}'.format(cmd, log_path)
    subprocess.call(cmd_execute, shell=True)

#---------------------------------------------------------------
# 初始化邮件
message = MIMEMultipart()

message['Subject'] = Header('End of Program notice: %s' % log_path, 'utf-8')
message['From'] = Header(add_from, 'utf-8')
message['To'] = Header(add_to, 'utf-8')

maintext = 'command: {}\nlog: {}'.format(cmd, log_path)

msg = MIMEText(maintext, 'plain', 'utf-8')
message.attach(msg)

#---------------------------------------------------------------
# 读取log文件
# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open(log_path, 'rb')
# Create a text/plain message
att1 = MIMEText(fp.read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename={}'.format(
    os.path.split(log_path)[-1])
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
