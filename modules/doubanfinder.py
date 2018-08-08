# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
from time import sleep
import sys
import json
import os
from bs4 import BeautifulSoup

class Doubanfinder(object):

	timeout = 10
	
	def __init__(self,showbrowser):
		display = Display(visible=0, size=(1600, 1024))
		display.start()
		if not showbrowser:
			os.environ['MOZ_HEADLESS'] = '1'
		self.driver = webdriver.Firefox()

		self.driver.delete_all_cookies()


	def doLogin(self,username,password):
			
		self.driver.get("https://www.douban.com/login")
		self.driver.execute_script('localStorage.clear();')
		
		if(self.driver.title.encode('utf8','replace').startswith("登录")):
			print "\n[+] Douban Login Page loaded successfully [+]"
			wbUsername = self.driver.find_element_by_id("email")
			wbUsername.send_keys(username)
			wbPassword = self.driver.find_element_by_id("password")
			wbPassword.send_keys(password)
			#self.driver.find_element_by_id("login_button").click()
			#self.driver.find_element_by_css_selector('a.submitBtn').click()
			self.driver.find_element_by_css_selector('input[type=\'submit\']').click()
			sleep(5)
			if(self.driver.title.encode('utf8','replace').startswith("豆") == False):
				print "[+] Douban Login Success [+]\n"
			else:
				print "[-] Douban Login Failed [-]\n"


	def getDoubanProfiles(self,first_name,last_name):
		#try:
		url = "https://www.douban.com/search?cat=1005&q=" + first_name + "+" + last_name
		self.driver.get(url)
		sleep(3)
		searchresponse = self.driver.page_source.encode('utf-8')
		soupParser = BeautifulSoup(searchresponse, 'html.parser')
		picturelist = []

		for element in soupParser.find_all('div', {'class': 'pic'}):
			try:
				badlink = element.find('a')['href']
				link = badlink.split('?url=', 1)[1].split('&query', 1)[0].replace("%3A",":").replace("%2F","/")
				badprofilepiclinksmall = element.find('img')['src']
				profilepic = badprofilepiclinksmall.replace("/icon/u","/icon/ul")
				picturelist.append([link,profilepic,1.0])
			except Exception as e:
				print "Error"
				print e
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
	def getDoubanProfiles(self,first_name,last_name):
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


