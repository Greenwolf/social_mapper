# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import sys
from time import sleep

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options

method_map = {
    "username": "account-tab-account",
    "phone": "account-tab-phone"
}


class Doubanfinder(object):
    timeout = 10
    authentication_method = "username"

    def __init__(self, showbrowser):
        if sys.platform == "darwin":
            display = Display(visible=0, size=(1600, 1024))
            display.start()
        opts = Options()
        if not showbrowser:
            os.environ['MOZ_HEADLESS'] = '1'
            opts.headless = True
        else:
            opts.headless = False
        firefoxprofile = webdriver.FirefoxProfile()
        firefoxprofile.set_preference("permissions.default.desktop-notification", 1)
        firefoxprofile.set_preference("dom.webnotifications.enabled", 1)
        firefoxprofile.set_preference("dom.push.enabled", 1)
        self.driver = webdriver.Firefox(options=opts,
                                        firefox_profile=firefoxprofile,
                                        firefox_binary=os.environ.get("FIREFOX_BINARY", None),
                                        executable_path=os.environ.get("GECKODRIVER", None))
        self.driver.implicitly_wait(15)
        self.driver.delete_all_cookies()

    def doLogin(self, username, password):

        self.driver.get("https://www.douban.com")
        self.driver.execute_script('localStorage.clear();')
        sleep(3)  # waiting an iframe
        if (self.driver.title.encode('utf8', 'replace').startswith(bytes("豆瓣", 'utf-8'))):
            print("\n[+] Douban Login Page loaded successfully [+]")
            if not self.is_login_page():
                print("[+] Douban Login not found a login form. Exit... [+]")
                return False
            self.switch_to_login_iframe()
            self.change_signin_method(self.authentication_method)
            sleep(1)  # waiting a document changed
            # fill form
            self.driver.find_element_by_id("username").send_keys(username)
            self.driver.find_element_by_id("password").send_keys(password)
            # submit
            self.driver.find_element_by_xpath("//div[contains(@class, 'account-form-field-submit')]").click()
            sleep(5)
            self.driver.switch_to.default_content()
            if self.is_login_page():
                print("[-] Douban Login Failed [-]\n")
            else:
                print("[+] Douban Login Success [+]\n")
        else:
            print("[-] Douban Login Page loaded error [-]")

    def _fetch_login_frame(self):
        iframes = self.driver.find_elements_by_tag_name("iframe")
        return next((x for x in iframes if "accounts.douban.com/passport/login_popup" in x.get_attribute("src")))

    def change_signin_method(self, method: 'phone|username' = 'username'):
        try:
            xpath = f"//div[@class='account-body-tabs']/ul[@class='tab-start']/li[contains(@class, '{method_map[method]}')]"
        except KeyError:
            print(f"authentication method `{method}` not support... {method_map.keys()}")
        else:
            self.driver.find_element_by_xpath(xpath).click()

    def is_login_page(self):
        """checking for a anony iframe is exists on page"""
        try:
            self._fetch_login_frame()
        except (NoSuchElementException, StopIteration):
            return False
        else:
            return True

    def switch_to_login_iframe(self):
        frame = self._fetch_login_frame()
        self.driver.switch_to.frame(frame)

    def getDoubanProfiles(self, first_name, last_name):
        # try:
        url = "https://www.douban.com/search?cat=1005&q=" + first_name + "+" + last_name
        self.driver.get(url)
        sleep(3)
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        picturelist = []

        for element in soupParser.find_all('div', {'class': 'pic'}):
            try:
                badlink = element.find('a')['href']
                link = badlink.split('?url=', 1)[1].split('&query', 1)[0].replace("%3A", ":").replace("%2F", "/")
                badprofilepiclinksmall = element.find('img')['src']
                profilepic = badprofilepiclinksmall.replace("/icon/u", "/icon/ul")
                picturelist.append([link, profilepic, 1.0])
            except Exception as e:
                print("Error")
                print(e)
                continue
        return picturelist

    # except Exception as e:
    #    picturelist = []
    #    print "Error"
    #    print e
    #    return picturelist

    def kill(self):
        self.driver.quit()

    # def getDoubanProfiles(self, first_name, last_name):
    #     url = "https://www.vkontakte.com/search/people/?q=" + first_name + "%20" + last_name
    #     self.driver.get(url)
    #     sleep(3)
    #     searchresponse = self.driver.page_source.encode('utf-8')
    #     soupParser = BeautifulSoup(searchresponse, 'html.parser')
    #     picturelist = []
    #     for element in soupParser.find_all('div', {'class': '_52eh _ajx'}):
    #         link = element.find('a')['href']
    #         picturelist.append([link, 1.0])
    #     return picturelist
    #
    # def getProfilePicture(self, profilelink):
    #     try:
    #         self.driver.get(profilelink)
    #         sleep(3)
    #         profileresponse = self.driver.page_source.encode('utf-8')
    #         soupParser = BeautifulSoup(profileresponse, 'html.parser')
    #         linktobigpic = ""
    #         for element in soupParser.find_all('div', {'class': 'photoContainer'}):
    #             linktobigpic = element.find('a')['href']
    #
    #         # if linktobigpic.startswith("/")
    #         # return ""
    #         self.driver.get(linktobigpic)
    #         sleep(3)
    #         bigpicresponse = self.driver.page_source.encode('utf-8')
    #         soupParser = BeautifulSoup(bigpicresponse, 'html.parser')
    #         image_link = ""
    #         for element in soupParser.find_all('div', {'class': '_2-sx'}):
    #             image_link = element.find('img')['src']
    #         return image_link
    #     except:
    #         return ""
