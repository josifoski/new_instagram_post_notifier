#! /usr/bin/env python3.5
# by Aleksandar Josifoski https://about.me/josifsk
# Script for checking new instagram posts for instagram.com/user, sending notify email
# 2017 February 10

import sys
import requests
import re
import smtplib
import datetime
import codecs
import html
import logging

user = ''

dir_in = '/data/Scrape/instagram_facebook/' # Change dir_in where script will be

logging.basicConfig(filename=dir_in + 'instagram.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

url="https://instagram.com/" + user.strip()

try:
    with open(dir_in + "last_instagram_media_count") as f_last_instagram_media_count:
        last_media_count = f_last_instagram_media_count.read().strip()
except:
    last_media_count = "0"

req = requests.get(url)
page_source = html.unescape(req.text)
# eventual part for saving page_source in file for analysis
with codecs.open(dir_in + 'page_source.txt', 'w') as fps:
    fps.write(page_source)

# sending email.
email_address_from = ''
email_address_to = ['']
password = ''
smtpServer = 'mail.smtp2go.com'
port = '587'

def sendemailnotify(lvsmtpServer, lvport, lvemail_address_from, lvpassword, lvemail_address_to):
    showPrintMessages = False
    try:
        smtpObj = smtplib.SMTP(lvsmtpServer, lvport)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(lvemail_address_from, lvpassword)
    except Exception as esc:
        print(str(esc))
        logging.debug(str(esc))

    FROM = lvemail_address_from
    TO =  lvemail_address_to
    SUBJECT = 'New instagram post by %s!' % user
    link = ''
    TEXT = ''
    message = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)

    now = str(datetime.datetime.now())[:16]
    try:
        smtpObj.sendmail(FROM, TO, message)
        print(now + ': notification email sent')
        logging.debug('notification email sent')
        smtpObj.quit()
    except Exception as esc:
        print(str(esc))
        logging.debug(str(esc))

medialine = page_source.split('"media":')[1].strip().split('\n')[0]
left = 0
ind = -1
for ch in medialine:
    ind += 1
    if ch == '{':
        left += 1
    if ch == '}':
        left -= 1
    if left == 0:
        thisis = ind
        break
        
goingon = medialine[:thisis + 1]
goingon = goingon.replace('false', 'False')
goingon = goingon.replace('true', 'True')
goingon = goingon.replace('null', 'None')
dddict = eval(goingon)
current_media_count = str(dddict["count"]).strip()
print("media count", current_media_count)

if current_media_count != last_media_count:
    sendemailnotify(smtpServer, port, email_address_from, password, email_address_to)
    with open(dir_in + "last_instagram_media_count", "w") as g:
        g.write(current_media_count)
    logging.debug('New post!')
else:
    logging.debug('no new post')
    print('no new post')
