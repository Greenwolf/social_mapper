from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from time import sleep
import sys
import os
import re
from bs4 import BeautifulSoup

class Instagramfinder(object):

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
			
		self.driver.get("https://instagram.com/accounts/login/")
		self.driver.execute_script('localStorage.clear();')

		#convert unicode in instagram title to spaces for comparison
		titleString = ''.join([i if ord(i) < 128 else ' ' for i in self.driver.title])

		if(titleString.startswith("Login")):
			print "\n[+] Instagram Login Page loaded successfully [+]"
			instagramUsername = self.driver.find_element_by_xpath("//input[@name='username']")
			instagramUsername.send_keys(username)
			instagramPassword = self.driver.find_element_by_xpath("//input[@name='password']")
			instagramPassword.send_keys(password)
			self.driver.find_element_by_xpath("//button[contains(.,'Log in')]").click()
			#self.driver.find_element_by_class_name("submit").click()
			#self.driver.find_element_by_css_selector("button.submit.btn.primary-btn").click()
			sleep(5)
			if(str(self.driver.title.encode('utf8','replace')).startswith("Instagram") == True):
				print "[+] Instagram Login Success [+]\n"
			else:
				print "[-] Instagram Login Failed [-]\n"


	def getInstagramProfiles(self,first_name,last_name,username,password):
		try:
			url = "https://www.instagram.com/"
			self.driver.get(url)
			sleep(3)
			#searchbar = self.driver.find_element_by_xpath("//body")
			#searchbar.send_keys(Keys.TAB)
			#searchbar = self.driver.find_element_by_class_name("_avvq0").click()
			picturelist = []	
			try:
				searchbar = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
			except:
				#if cant find search bar try to relogin
				self.doLogin(username,password)
				self.driver.get(url)
				sleep(3)
				try:
					searchbar = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
				except:
					print "Instagram Timeout Error, session has expired and attempts to reestablish have failed"
					return picturelist
			sleep(1)
			full_name = first_name + " " + last_name
			searchbar.send_keys(full_name)
			sleep(1)
			searchresponse = self.driver.page_source.encode('utf-8')
			sleep(1)
			soupParser = BeautifulSoup(searchresponse, 'html.parser')

			#for element in soupParser.find_all('a', {'class': '_ndl3t'}):
			for element in soupParser.find_all('a', {'class': 'yCE8d'}):
				#print element
				link = element['href']
				try:
					#profilepic = element.find('img')['src']
					#print profilepic
					# Errors with instagram https://github.com/stevenschobert/instafeed.js/issues/549

					# Old code for getting a bigger instagram profile picture, doesnt work since March 23rd 2018
					#profilepicwithsmallid = element.find('img')['src']
					#if not "150x150" in profilepicwithsmallid:
					#	continue
					#profilepicbadurl = profilepicwithsmallid.replace('150x150', '600x600')
					#profilepic = profilepicbadurl.split("/")[0] + "//" + profilepicbadurl.split("/")[2] + "/" + profilepicbadurl.split("/")[6] + "/" + profilepicbadurl.split("/")[7] + "/" + profilepicbadurl.split("/")[8] 
					
					# New code for getting instagram profile pic, if possible make it better with a bigger image, but may not be possible anymore
					profilepic = element.find('img')['src']

					picturelist.append(["https://instagram.com" + link, profilepic,1.0])
				except:
					#The find imgsrc fails on search items that arn't profiles so we catch and continue
					continue
				
			return picturelist
		except Exception as e: 
			print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + e
			picturelist = []
			#print "Error"
			return picturelist

	def testdeletecookies(self):
		self.driver.delete_all_cookies()

	def kill(self):
		self.driver.quit()
