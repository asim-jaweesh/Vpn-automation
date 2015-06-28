#!/usr/bin/env python
import pexpect
import mechanize
import sys 
from bs4 import BeautifulSoup
import argparse
import signal 
import os
import time
from subprocess import call

## BEGIN

verbose = 0


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# signal handler to exit gracefully 
def receive_signal(signal, frame):
	print ""
	print bcolors.OKGREEN + '[+]Exiting' + bcolors.OKGREEN
	call(["pkill","openvpn"])
	exit()
# register the handler
signal.signal(signal.SIGINT, receive_signal)

# cli args
parser = argparse.ArgumentParser(description="vpn.py certfile.ovpn")
parser.add_argument('-c', type=str, help="OpenVpn Certificate file", required=True)
parser.add_argument('--verbose',help="Verbose output", action="store_true")

# grab vpn password from vpnbook website
def password() : 
	br = mechanize.Browser()
	br.open("http://www.vpnbook.com/freevpn")
	a = br.response().read()
	bt = BeautifulSoup(a , "lxml")
	link = bt.find_all("li")
	passw = link[-1].text
	password = str(passw.split(":")[1][1:])
	return  password

cmdargs = parser.parse_args()
#verbose = cmdargs.v
confFile = cmdargs.c

# run openvpn and connect
print bcolors.OKGREEN + "[+] Starting" + bcolors.OKGREEN
vpn = pexpect.spawn("openvpn " + confFile)
vpn.timeout=300000000000
vpn.expect("Username:")
vpn.sendline("vpnbook")
vpn.expect("Password:")
a = password()
vpn.sendline(a)
while 1 :
	if cmdargs.verbose:
		print  bcolors.OKBLUE + vpn.readline() + bcolors.OKBLUE
	
	if "Completed" in vpn.readline() :
		print bcolors.OKGREEN + "[+] Connected" + bcolors.OKGREEN
		break  

while 1 :
	pass



## END
