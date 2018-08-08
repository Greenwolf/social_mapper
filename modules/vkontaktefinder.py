from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
from time import sleep
import sys
import json
import os
from bs4 import BeautifulSoup

class Vkontaktefinder(object):

	timeout = 10
	
	def __init__(self,showbrowser):
		display = Display(visible=0, size=(1600, 1024))
		display.start()
		if not showbrowser:
			os.environ['MOZ_HEADLESS'] = '1'
		self.driver = webdriver.Firefox()

		self.driver.delete_all_cookies()


	def doLogin(self,username,password):
			
		self.driver.get("https://www.vk.com/login")
		self.driver.execute_script('localStorage.clear();')
		
		if(str(self.driver.title).encode('ascii','replace').startswith("Log in")):
			print "\n[+] VKontakte Login Page loaded successfully [+]"
			vkUsername = self.driver.find_element_by_id("email")
			vkUsername.send_keys(username)
			vkPassword = self.driver.find_element_by_id("pass")
			vkPassword.send_keys(password)
			self.driver.find_element_by_id("login_button").click()
			sleep(10)
			if(str(self.driver.title).encode('ascii','replace').startswith("Log in") == False):
				print "[+] Vkontakte Login Success [+]\n"
			else:
				print "[-] Vkontakte Login Failed [-]\n"


	def getVkontakteProfiles(self,first_name,last_name):
		#try:
		url = "https://vk.com/search?c%5Bq%5D=" + first_name + "%20" + last_name + "&c%5Bsection%5D=auto"
		self.driver.get(url)
		sleep(3)
		searchresponse = self.driver.page_source.encode('utf-8')
		soupParser = BeautifulSoup(searchresponse, 'html.parser')
		picturelist = []

		for element in soupParser.find_all('div', {'class': 'people_row'}): # "people_row search_row clear_fix"
			try:
				link = element.find('a')['href']
				profilepic = element.find('img')['src']
				picturelist.append(["https://vk.com" + link,profilepic,1.0])
			except:
				continue
		return picturelist
		#except Exception as e:
		#	picturelist = []
		#	print "Error"
		#	print e
		#	return picturelist

	def kill(self):
		self.driver.quit()

'''
	def getVkontakteProfiles(self,first_name,last_name):
		url = "https://www.vkontakte.com/search/people/?q=" + first_name + "%20" + last_name
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


