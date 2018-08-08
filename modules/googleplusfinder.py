# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
from time import sleep
import sys
import json
import os
from bs4 import BeautifulSoup

class GooglePlusfinder(object):

	timeout = 10
	
	def __init__(self,showbrowser):
		display = Display(visible=0, size=(1600, 1024))
		display.start()
		if not showbrowser:
			os.environ['MOZ_HEADLESS'] = '1'
		self.driver = webdriver.Firefox()

		self.driver.delete_all_cookies()


	def doLogin(self,username,password):
		self.driver.set_page_load_timeout(15)
		try:
			self.driver.get("https://plus.google.com/discover")
		except:
			pass
		self.driver.execute_script('localStorage.clear();')	
		
		
		if(self.driver.title.encode('utf8','replace').startswith("Discover")):
			print "\n[+] Google Login Page Part 1 loaded successfully [+]"
			self.driver.find_element_by_id("gb_70").click()
			sleep(5)
			if(self.driver.title.encode('utf8','replace').startswith("Sign")):
				print "[+] Google Login Page Part 2 loaded successfully [+]"
				gpUsername = self.driver.find_element_by_id("identifierId")
				gpUsername.send_keys(username)
				try:
					self.driver.find_element_by_id("identifierNext").click()
				except:
					pass
				sleep(5)
				print "[+] Google Login Page Part 3 loaded successfully [+]"
				gpPassword = self.driver.find_element_by_class_name("Xb9hP")
				gpPassword.send_keys(password)
				try:
					self.driver.find_element_by_id("passwordNext").click()
				except:
					pass
				#self.driver.find_element_by_id("login_button").click()
				#self.driver.find_element_by_css_selector('a.submitBtn').click()
				#self.driver.find_element_by_css_selector('a[node-type=\'submitBtn\']').click()
				sleep(5)
				if(self.driver.title.encode('utf8','replace').startswith("Discover")):
					print "[+] GooglePlus Login Success [+]\n"
				else:
					print "[-] GooglePlus Login Failed [-]\n"


	def getGooglePlusProfiles(self,first_name,last_name):
		#try:
		url = "https://plus.google.com/s/" + first_name + "%20" + last_name + "/people"
		self.driver.get(url)
		sleep(3)
		picturelist = []
		searchresponse = self.driver.page_source.encode('utf-8')
		soupParser = BeautifulSoup(searchresponse, 'html.parser')
		for element in soupParser.find_all('div', {'class': 'NzRmxf'}): # "people_row search_row clear_fix"
			try:
				badlink = element.find('a')['href']
				link = badlink.replace("./","https://plus.google.com/")
				badprofilepiclinkseventytwo = element.find('img')['src']
				profilepic = badprofilepiclinkseventytwo.replace("/s72","/s1000").replace("/s36","/s1000").replace("/s180","/s1000")
				picturelist.append([link,profilepic,1.0])
			except Exception as e:
				print "Error"
				print e
				continue
		#print picturelist
		unique_picturelist = [list(x) for x in set(tuple(x) for x in picturelist)]
		#print unique_picturelist
		return unique_picturelist
		#except Exception as e:
		#	picturelist = []
		#	print "Error"
		#	print e
		#	return picturelist

	def kill(self):
		self.driver.quit()

'''
	def getGooglePlusProfiles(self,first_name,last_name):
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


