import mechanize , pexpect  , sys 
from bs4 import BeautifulSoup
usage = ''' 
usage : python vpn.py 'cert file' 
'''
if len(sys.argv) < 2 : 
	print usage
	exit(1) 
def password() : 
	br = mechanize.Browser()
	br.open("http://www.vpnbook.com/freevpn")
	a = br.response().read()
	bt = BeautifulSoup(a , "lxml")
	link = bt.find_all("li")
	passw = link[-1].text
	password = str(passw.split(":")[1][1:])
	return  password
vpn = pexpect.spawn("openvpn "+str(sys.argv[1]))
vpn.timeout=300000000000
vpn.expect("Username:")
vpn.sendline("vpnbook")
vpn.expect("Password:")
a = password()
vpn.sendline(a)
print "[*] Starting ... " 
while 1 :
	if "Completed" in vpn.next() : break  
	else : print  vpn.next()  


while 1 : 
	pass
