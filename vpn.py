#!/usr/bin/python
import mechanize , pexpect  , sys ,signal
def signal_handler(signal, frame):
    print "\n[-] Exiting"
    exit()
signal.signal(signal.SIGINT, signal_handler)
from bs4 import BeautifulSoup
usage = ''' 
[+] usage : python vpn.py 'cert file' 
'''
if len(sys.argv) < 2 : 
	print usage
	exit(1)
print "[*] Starting ... " 
def password() : 
	br = mechanize.Browser()
	br.open("http://www.vpnbook.com/freevpn")
	a = br.response().read()
	bt = BeautifulSoup(a , "lxml")
	link = bt.find_all("li")
	passw = link[-1].text
	password = str(passw.split(":")[1][1:])
	return  password
try :
	vpn = pexpect.spawn("openvpn vpnbook-euro1-tcp80.ovpn")
	vpn.timeout=300000000000
	vpn.expect("Username:")
	vpn.sendline("vpnbook")
	vpn.expect("Password:")
	a = password()
	vpn.sendline(a)
	print "[+] Password : "+a
	while 1 :
		if "Completed" in vpn.next() : break  
		else : print  vpn.next()  


	while 1 : 
		pass
except : 
	print "[-] Something went wrong :/ "
	sys.exit(1)
