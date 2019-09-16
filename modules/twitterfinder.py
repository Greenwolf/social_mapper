from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from time import sleep
import traceback
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
		firefoxprofile = webdriver.FirefoxProfile()
		firefoxprofile.set_preference("permissions.default.desktop-notification", 1)
		firefoxprofile.set_preference("dom.webnotifications.enabled", 1)
		firefoxprofile.set_preference("dom.push.enabled", 1)
		self.driver = webdriver.Firefox(firefox_profile=firefoxprofile)
		self.driver.implicitly_wait(15)
		self.driver.delete_all_cookies()


	def doLogin(self,username,password):

		self.driver.get("https://twitter.com/login")
		self.driver.execute_script('localStorage.clear();')

		#agent = self.driver.execute_script("return navigator.userAgent")
		#print("User Agent: " + agent)
		
		if(self.driver.title.encode('ascii','replace').startswith(bytes("Login on", 'utf-8'))):
			print("\n[+] Twitter Login Page loaded successfully [+]")
			try:
				twUsername = self.driver.find_element_by_class_name("js-username-field")
			except:
				print("Twitter Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
				sys.exit()
			twUsername.send_keys(username)
			sleep(2)

			try:
				#twPassword = self.driver.find_element_by_xpath("//input[@class='js-password-field']")
				twPassword = self.driver.find_element_by_class_name("js-password-field")
			except:
				print("Twitter Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
				sys.exit()
			twPassword.send_keys(password)
			sleep(2)

			try:
				twLoginButton = self.driver.find_element_by_xpath("//button[@class='submit EdgeButton EdgeButton--primary EdgeButtom--medium']")
			except:
				print("Twitter Login Page login button name seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
				traceback.print_exc()
				sys.exit()
			twLoginButton.click()
			sleep(5)

			if(self.driver.title.encode('ascii','replace').startswith(bytes("Login on", 'utf-8'))):
				print("[-] Twitter Login Failed [-]\n")
			else:
				print("[+] Twitter Login Success [+]\n")
		else:
			print("Twitter Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")


	def getTwitterProfiles(self,first_name,last_name):
		#url = "https://twitter.com/search?f=users&vertical=default&q=" + first_name + "%20" + last_name + "&src=typd"
		url = "https://twitter.com/search?q=" + first_name + "%20" + last_name + "&src=typd&f=user"
		self.driver.get(url)
		sleep(3)
		searchresponse = self.driver.page_source.encode('utf-8')
		soupParser = BeautifulSoup(searchresponse, 'html.parser')
		picturelist = []
		#for element in soupParser.find_all('div', {'class': 'ProfileCard-content'}):
		for element in soupParser.find_all('div', {'class': 'css-18t94o4 css-1dbjc4n r-1j3t67a r-1w50u8q r-o7ynqc r-1j63xyz'}):
			try:
				link = element.find('a')['href']
				smallpic = element.find('img')['src']
				#replaced1 = smallpic.replace("_bigger.jpg","_400x400.jpg")
				#profilepic = replaced1.replace("_bigger.jpeg","_400x400.jpg")
				profilepic = smallpic.replace("_reasonably_small.","_400x400.")
				picturelist.append(["https://twitter.com" + link,profilepic,1.0])
				#print("https://twitter.com" + link + "\n" + profilepic)
			except:
				print("Error")
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



