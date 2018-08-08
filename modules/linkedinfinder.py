from selenium import webdriver
from pyvirtualdisplay import Display
from time import sleep
import os
import sys
from bs4 import BeautifulSoup

class Linkedinfinder(object):

	timeout = 10
	
	def __init__(self,showbrowser):
		display = Display(visible=0, size=(1600, 1024))
		display.start()
		if not showbrowser:
			os.environ['MOZ_HEADLESS'] = '1'
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(15)
		self.driver.delete_all_cookies()


	def doLogin(self,username,password):
			
		self.driver.get("https://www.linkedin.com/uas/login")
		self.driver.execute_script('localStorage.clear();')
		
		if(str(self.driver.title).encode('ascii','replace').startswith("Sign In")):
			print "\n[+] LinkedIn Login Page loaded successfully [+]"
			lnkUsername = self.driver.find_element_by_id("session_key-login")
			lnkUsername.send_keys(username)
			lnkPassword = self.driver.find_element_by_id("session_password-login")
			lnkPassword.send_keys(password)
			self.driver.find_element_by_id("btn-primary").click()
			sleep(5)
			if(str(self.driver.title).encode('utf8','replace') == "LinkedIn"):
				print "[+] LinkedIn Login Success [+]\n"
			else:
				print "[-] LinkedIn Login Failed [-]\n"


	def getLinkedinProfiles(self,first_name,last_name,username,password):
		url = "https://www.linkedin.com/search/results/people/?keywords=" + first_name + "%20" + last_name + "&origin=SWITCH_SEARCH_VERTICAL"
		self.driver.get(url)
		sleep(3)
		picturelist = []
		if "login" in self.driver.current_url: 
			self.doLogin(username,password)
			self.driver.get(url)
			sleep(3)
			if "login" in self.driver.current_url: 
				print "LinkedIn Timeout Error, session has expired and attempts to reestablish have failed"
				return picturelist	
		searchresponse = self.driver.page_source.encode('utf-8')
		soupParser = BeautifulSoup(searchresponse, 'html.parser')
		picturelist = []
		for element in soupParser.find_all('div', {'class': 'search-result__image-wrapper'}):
			try:
				# check for ghost-person tag in img class to skip headless profiles
				#ghostcheck = element.find('div')['class'] - OLD
				ghostcheck = element.find_all('div')[1]['class']
				#print ghostcheck
				if "ghost-person" not in ghostcheck:
					link = element.find('a')['href']

					#profilepic = element.find('img')['src'] - OLD
					#profilepicreplaced = profilepic.replace("/mpr/mpr/shrink_100_100/","/media/") - OLD
					profilepic = element.find_all('div')[1]['style']
					profilepicreplaced = profilepic.replace("background-image: url(\"","").replace("\");","")
					picturelist.append(["https://linkedin.com" + link,profilepicreplaced,1.0])
			#except Exception as e:
			except:
				#print "Error"
				#print e
				continue
		return picturelist

	def testdeletecookies(self):
		self.driver.delete_all_cookies()

	def kill(self):
		self.driver.quit()


