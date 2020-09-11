from __future__ import print_function

import os
import sys
import traceback
from time import sleep

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Pinterestfinder(object):
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

        self.driver.get("https://www.pinterest.com/login/")
        self.driver.execute_script('localStorage.clear();')

        if (self.driver.title.encode('ascii', 'replace').startswith(bytes("Pinterest", 'utf-8'))):
            print("\n[+] Pinterest Login Page loaded successfully [+]")
            try:
                pinUsername = self.driver.find_element_by_id("email")
            except:
                print(
                    "Pinterest Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
                sys.exit()
            pinUsername.send_keys(username)
            sleep(2)

            try:
                # pinPassword = self.driver.find_element_by_xpath("//input[@class='js-password-field']")
                pinPassword = self.driver.find_element_by_id("password")
            except:
                print(
                    "Pinterest Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
                sys.exit()
            pinPassword.send_keys(password)
            sleep(2)

            try:
                pinLoginButton = self.driver.find_element_by_xpath("//button[@class='red SignupButton active']")
            except:
                print(
                    "Pinterest Login Page login button name seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
                traceback.print_exc()
                sys.exit()
            pinLoginButton.click()
            sleep(5)
            
            if (self.driver.title[0] == "("):
                print("[+] Pinterest Login Success [+]\n")
            else:
                try:
                    if (self.driver.title.split()[1] == "Login"):
                        print("[-] Pinterest Login Failed [-]\n")
                    else:
                        print("[+] Pinterest Login Success [+]\n")
                except:
                    print("[+] Pinterest Login Success [+]\n")
        else:
            print(
                "Pinterest Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")

    def getPinterestProfiles(self, first_name, last_name):
        url = "https://www.pinterest.de/search/users/?q=" + first_name + "%20" + last_name
        self.driver.get(url)
        sleep(3)
        searchresponse = self.driver.page_source.encode('utf-8')
        soupParser = BeautifulSoup(searchresponse, 'html.parser')
        picturelist = []
        for element in soupParser.find_all('div', {'class': 'Yl-'}):
            try:
                link = element.find('a')['href']
                smallpic = element.find('img')['src']
                # replaced1 = smallpic.replace()
                # profilepic = replaced1.replace("_bigger.jpeg","_400x400.jpg")
                picturelist.append(["https://pinterest.com" + link, smallpic, 1.0])
            # print(smallpic)
            except:
                continue
        return picturelist

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
