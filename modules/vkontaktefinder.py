from __future__ import print_function
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

    def __init__(self, showbrowser):
        display = Display(visible=0, size=(1600, 1024))
        display.start()
        if not showbrowser:
            os.environ['MOZ_HEADLESS'] = '1'
        firefoxprofile = webdriver.FirefoxProfile()
        firefoxprofile.set_preference(
            "permissions.default.desktop-notification", 1)
        firefoxprofile.set_preference("dom.webnotifications.enabled", 1)
        firefoxprofile.set_preference("dom.push.enabled", 1)
        self.driver = webdriver.Firefox(firefox_profile=firefoxprofile)
        self.driver.implicitly_wait(15)
        self.driver.delete_all_cookies()

    def doLogin(self, username, password):

        self.driver.get("https://www.vk.com/login")
        self.driver.execute_script('localStorage.clear();')

        if(self.driver.title.encode('ascii', 'replace').startswith(bytes("Log in", 'utf-8'))):
            print("\n[+] VKontakte Login Page loaded successfully [+]")
            vkUsername = self.driver.find_element_by_id("email")
            vkUsername.send_keys(username)
            vkPassword = self.driver.find_element_by_id("pass")
            vkPassword.send_keys(password)
            self.driver.find_element_by_id("login_button").click()
            sleep(10)
            if(self.driver.title.encode('ascii', 'replace').startswith(bytes("Log in", 'utf-8')) == False):
                print("[+] Vkontakte Login Success [+]\n")
            else:
                print("[-] Vkontakte Login Failed [-]\n")

    def getVkontakteProfiles(self, first_name, last_name):
        # try:
        url = "https://vk.com/search?c%5Bq%5D=" + first_name + \
            "%20" + last_name + "&c%5Bsection%5D=auto"
        self.driver.get(url)
        sleep(3)
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        picturelist = []

        # "people_row search_row clear_fix"
        for element in soupParser.find_all('div', {'class': 'people_row'}):
            try:
                link = element.find('a')['href']
                profilepic = element.find('img')['src']
                picturelist.append(["https://vk.com" + link, profilepic, 1.0])
            except:
                continue
        return picturelist

    def kill(self):
        self.driver.quit()
