from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
from time import sleep
import sys
import json
import os
from bs4 import BeautifulSoup

class Facebookfinder(object):

	timeout = 10
	
	def __init__(self,showbrowser):
		display = Display(visible=0, size=(1600, 1024))
		display.start()
		if not showbrowser:
			os.environ['MOZ_HEADLESS'] = '1'
		self.driver = webdriver.Firefox()

		self.driver.delete_all_cookies()


	def doLogin(self,username,password):
			
		self.driver.get("https://www.facebook.com/login")
		self.driver.execute_script('localStorage.clear();')
		
		if(str(self.driver.title).encode('ascii','replace').startswith("Log in")):
			print "\n[+] Facebook Login Page loaded successfully [+]"
			fbUsername = self.driver.find_element_by_id("email")
			fbUsername.send_keys(username)
			fbPassword = self.driver.find_element_by_id("pass")
			fbPassword.send_keys(password)
			self.driver.find_element_by_id("loginbutton").click()
			sleep(5)
			# checks if a notification is in place, which changes the title
			if (self.driver.title.encode('utf8','replace')[0] == "("):
				if(str(self.driver.title.encode('utf8','replace').split()[1]) == "Facebook"):
					print "[+] Facebook Login Success [+]\n"
				else:
					print "[-] Facebook Login Failed [-]\n"
			else:
				if(self.driver.title.encode('utf8','replace').startswith("Facebook") == True):
					print "[+] Facebook Login Success [+]\n"
				else:
					print "[-] Facebook Login Failed [-]\n"


	def getFacebookProfiles(self,first_name,last_name,username,password):
		#try:
		url = "https://www.facebook.com/search/people/?q=" + first_name + "%20" + last_name
		self.driver.get(url)
		sleep(3)
		picturelist = []
		#print ""
		#print "TEST"
		#print "firstname: "
		#print first_name
		#print "title: "
		#print self.driver.title.encode('utf8','replace').split()[1]
		#print "END TEST"
		# checks if word after space (for when a notifaction changes the title) or the first word is not equal to the first name being searched, meaning the session has timed out
		if(self.driver.title.encode('utf8','replace').split()[1].startswith(first_name) == False and self.driver.title.encode('utf8','replace').startswith(first_name) == False): 
			print "\nFacebook session has expired attempting to reestablish..."
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if(self.driver.title.encode('utf8','replace').split()[1].startswith(first_name) == False and self.driver.title.encode('utf8','replace').startswith(first_name) == False): 
				print "Facebook Timeout Error, session has expired and attempts to reestablish have failed"
				return picturelist
			else:
				print "New Facebook Session created, resuming mapping process"
		searchresponse = self.driver.page_source.encode('utf-8')
		soupParser = BeautifulSoup(searchresponse, 'html.parser')

		for element in soupParser.find_all('div', {'class': '_401d'}):
			try:
				datagt = element['data-gt']
				stripped = datagt.replace("\\","")
				stripped2 = stripped.replace("{\"type\":\"xtracking\",\"xt\":\"21.","")
				stripped3 = stripped2.replace("}\"}","}")
				jsondata = json.loads(stripped3)
				profilepic = "https://www.facebook.com/search/async/profile_picture/?fbid=" + str(jsondata['raw_id']) + "&width=8000&height=8000"
				link = element.find('a')['href']
				cdnpicture = element.find('img')['src']
				picturelist.append([link,profilepic,1.0,cdnpicture])
			except:
				continue
		return picturelist
		#except Exception as e:
		#	picturelist = []
		#	print "Error"
		#	print e
		#	return picturelist

	def getCookies(self):
		all_cookies = self.driver.get_cookies()
		cookies = {}
		for s_cookie in all_cookies:
			cookies[s_cookie["name"]]=s_cookie["value"]
		return cookies

	def testdeletecookies(self):
		self.driver.delete_all_cookies()


	def kill(self):
		self.driver.quit()

'''
	def getFacebookProfiles(self,first_name,last_name):
		url = "https://www.facebook.com/search/people/?q=" + first_name + "%20" + last_name
		self.driver.get(url)
		sleep(3)
		searchresponse = self.driver.page_source.encode('utf-8')
		soupParser = BeautifulSoup(searchresponse, 'html.parser')
		picturelist = []
		for element in soupParser.find_all('div', {'class': '_52eh _ajx'}):
			link = element.find('a')['href']
			picturelist.append([link,1.0])
		return picturelist


	def getProfilePicture(self, profilelink):
		try:	
			self.driver.get(profilelink)
			sleep(3)
			profileresponse = self.driver.page_source.encode('utf-8')
			soupParser = BeautifulSoup(profileresponse, 'html.parser')
			linktobigpic = ""
			for element in soupParser.find_all('div', {'class': 'photoContainer'}):
				linktobigpic = element.find('a')['href']

			#if linktobigpic.startswith("/")
				#return ""
			self.driver.get(linktobigpic)
			sleep(3)
			bigpicresponse = self.driver.page_source.encode('utf-8')
			soupParser = BeautifulSoup(bigpicresponse, 'html.parser')
			image_link = ""
			for element in soupParser.find_all('div', {'class': '_2-sx'}):
				image_link = element.find('img')['src']
			return image_link
		except:
			return ""
'''


