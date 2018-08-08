from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from time import sleep
import sys
import os
from bs4 import BeautifulSoup

class Twitterfinder(object):

	timeout = 10
	
	def __init__(self,showbrowser):
		display = Display(visible=0, size=(1600, 1024))
		display.start()
		if not showbrowser:
			os.environ['MOZ_HEADLESS'] = '1'
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(15)
		#self.driver.set_page_load_timeout(15)
		self.driver.delete_all_cookies()


	def doLogin(self,username,password):
			
		self.driver.get("https://twitter.com/login")
		self.driver.execute_script('localStorage.clear();')
		
		if(str(self.driver.title).encode('ascii','replace').startswith("Login on")):
			print "\n[+] Twitter Login Page loaded successfully [+]"
			twitterUsername = self.driver.find_element_by_class_name("js-username-field")
			twitterUsername.send_keys(username)
			twitterPassword = self.driver.find_element_by_class_name("js-password-field")
			twitterPassword.send_keys(password)
			twitterPassword.send_keys(Keys.ENTER)
			sleep(5)
			if(str(self.driver.title) == "Twitter"):
				print "[+] Twitter Login Success [+]\n"
			else:
				print "[-] Twitter Login Failed [-]\n"

	def getTwitterProfiles(self,first_name,last_name):
		url = "https://twitter.com/search?f=users&vertical=default&q=" + first_name + "%20" + last_name + "&src=typd"
		self.driver.get(url)
		sleep(3)
		searchresponse = self.driver.page_source.encode('utf-8')
		soupParser = BeautifulSoup(searchresponse, 'html.parser')
		picturelist = []
		for element in soupParser.find_all('div', {'class': 'ProfileCard-content'}):
			try:
				link = element.find('a')['href']
				smallpic = element.find('img')['src']
				replaced1 = smallpic.replace("_bigger.jpg","_400x400.jpg")
				profilepic = replaced1.replace("_bigger.jpeg","_400x400.jpg")
				picturelist.append(["https://twitter.com" + link,profilepic,1.0])
			except:
				print "Error"
				continue
		return picturelist



	def kill(self):
		self.driver.quit()

'''
	def getTwitterProfiles(self,first_name,last_name):
		url = "https://twitter.com/search?f=users&vertical=default&q=" + first_name + "%20" + last_name + "&src=typd"
		self.driver.get(url)
		sleep(3)
		searchresponse = self.driver.page_source.encode('utf-8')
		soupParser = BeautifulSoup(searchresponse, 'html.parser')
		picturelist = []
		for element in soupParser.find_all('div', {'class': 'ProfileCard'}):
			link = element.find('a')['href']
			picturelist.append(["https://twitter.com" + link,1.0])
		return picturelist


	def getProfilePicture(self, profilelink):
		try:	
			#print "Profile Link: " + profilelink
			# THIS IS SO SLOW????
			self.driver.get(profilelink)
			# Make it better?
			sleep(3)
			profileresponse = self.driver.page_source.encode('utf-8')
			soupParser = BeautifulSoup(profileresponse, 'html.parser')
			linktobigpic = ""
			for element in soupParser.find_all('img', {'class': 'ProfileAvatar-image'}):
				linktobigpic = element['src']
			return linktobigpic
		except:
			print "getProfilePicture EXCEPTION"
			return ""

'''



