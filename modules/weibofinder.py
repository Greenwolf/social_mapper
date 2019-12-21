# -*- coding: utf-8 -*-
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pyvirtualdisplay import Display
from time import sleep
import sys
import json
import os
from bs4 import BeautifulSoup


class Weibofinder(object):

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

        self.driver.get("https://weibo.com/login.php")
        self.driver.execute_script('localStorage.clear();')

        if(self.driver.title.encode('utf8', 'replace').startswith(bytes("微博", 'utf-8'))):
            print("\n[+] Weibo Login Page loaded successfully [+]")
            wbUsername = self.driver.find_element_by_id("loginname")
            wbUsername.send_keys(username)
            wbPassword = self.driver.find_element_by_name("password")
            wbPassword.send_keys(password)

            self.driver.find_element_by_css_selector(
                'a[node-type=\'submitBtn\']').click()
            sleep(5)
            if(self.driver.title.encode('utf8', 'replace').startswith(bytes("我的首页", 'utf-8')) == False):
                print("[+] Weibo Login Success [+]\n")
            else:
                print("[-] Weibo Login Failed [-]\n")

    def getWeiboProfiles(self, first_name, last_name):
        # try:
        url = "http://s.weibo.com/user/" + first_name + \
            "%2B" + last_name + "&Refer=weibo_user"
        self.driver.get(url)
        sleep(3)
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        picturelist = []

        # "people_row search_row clear_fix"
        for element in soupParser.find_all('div', {'class': 'person_pic'}):
            try:
                badlink = element.find('a')['href']
                link = badlink.replace("//weibo", "https://weibo")
                badprofilepiclinkoneeighty = element.find('img')['src']
                badprofilepic = badprofilepiclinkoneeighty.replace(
                    ".180/", ".5000/")
                profilepic = badprofilepic.replace("//", "http://")
                picturelist.append([link, profilepic, 1.0])
            except:
                continue
        return picturelist

    def kill(self):
        self.driver.quit()
