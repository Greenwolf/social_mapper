from __future__ import print_function

import json
import os
import sys
from time import sleep

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Facebookfinder(object):
    timeout = 10

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
        self.driver = webdriver.Firefox(firefox_profile=firefoxprofile, options=opts)

        self.driver.implicitly_wait(15)
        self.driver.delete_all_cookies()

    def doLogin(self, username, password):

        self.driver.get("https://www.facebook.com/login")
        self.driver.execute_script('localStorage.clear();')

        if (self.driver.title.encode('ascii', 'replace').endswith(bytes("Facebook", 'utf-8'))):
            print("\n[+] Facebook Login Page loaded successfully [+]")
            # click on accept cookies banner
            self.driver.find_element_by_xpath("//button[@data-testid='cookie-policy-banner-accept']").click()
            fbUsername = self.driver.find_element_by_id("email")
            fbUsername.send_keys(username)
            fbPassword = self.driver.find_element_by_id("pass")
            fbPassword.send_keys(password)
            self.driver.find_element_by_id("loginbutton").click()
            sleep(5)
            # checks if a notification is in place, which changes the title
            if (self.driver.title.encode('ascii', 'replace')[0] == bytes("(",'ascii')):
                if (str(self.driver.title.encode('ascii', 'replace').split()[1]) == bytes("Facebook", 'ascii')):
                    print("[+] Facebook Login Success [+]\n")
                else:
                    print("[-] Facebook Login Failed [-]\n")
            else:
                if (self.driver.title.encode('ascii', 'replace').startswith(bytes("Facebook", 'ascii')) == True):
                    print("[+] Facebook Login Success [+]\n")
                else:
                    print("[-] Facebook Login Failed [-]\n")

    def getFacebookProfiles(self, first_name, last_name, username, password):
        # try:
        url = "https://www.facebook.com/search/people/?q=" + first_name + "%20" + last_name
        self.driver.get(url)
        sleep(3)
        picturelist = []
        # print ""
        # print "TEST"
        # print "firstname: "
        # print first_name
        # print "title: "
        # print self.driver.title.encode('utf8','replace').split()[1]
        # print "END TEST"
        # checks if word after space (for when a notification changes the title) or the first word is not equal to the first name being searched, meaning the session has timed out

        if (self.driver.title.encode('utf8', 'replace').split()[1].startswith(
            bytes(first_name, 'utf-8')) == False and self.driver.title.encode('utf8', 'replace').startswith(
            bytes(first_name, 'utf-8')) == False):
            print("\nFacebook session has expired, attempting to reestablish...")
            self.doLogin(username, password)
            self.driver.get(url)
            sleep(3)
            if (self.driver.title.encode('utf8', 'replace').split()[1].startswith(
                bytes(first_name, 'utf-8')) == False and self.driver.title.encode('utf8', 'replace').startswith(
                bytes(first_name, 'utf-8')) == False):
                print("Facebook Timeout Error, session has expired and attempts to reestablish have failed")
                return picturelist
            else:
                print("New Facebook Session created, resuming mapping process")
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')

        for element in soupParser.find_all('div', {'class': '_401d'}):
            try:
                datagt = element['data-gt']
                stripped = datagt.replace("\\", "")
                stripped2 = stripped.replace("{\"type\":\"xtracking\",\"xt\":\"21.", "")
                stripped3 = stripped2.replace("}\"}", "}")
                jsondata = json.loads(stripped3)
                profilepic = "https://www.facebook.com/search/async/profile_picture/?fbid=" + str(
                    jsondata['raw_id']) + "&width=8000&height=8000"
                link = element.find('a')['href']
                cdnpicture = element.find('img')['src']
                picturelist.append([link, profilepic, 1.0, cdnpicture])
            except:
                continue
        return picturelist

    # except Exception as e:
    #    picturelist = []
    #    print "Error"
    #    print e
    #    return picturelist

    def getCookies(self):
        all_cookies = self.driver.get_cookies()
        cookies = {}
        for s_cookie in all_cookies:
            cookies[s_cookie["name"]] = s_cookie["value"]
        return cookies

    def testdeletecookies(self):
        self.driver.delete_all_cookies()

    def kill(self):
        self.driver.quit()

    # def getFacebookProfiles(self, first_name, last_name):
    #     url = "https://www.facebook.com/search/people/?q=" + first_name + "%20" + last_name
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
    #         # if linktobigpic.startswith(bytes("/")
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
