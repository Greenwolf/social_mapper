from __future__ import print_function

import os
import sys
from time import sleep

from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Instagramfinder(object):
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
        self.driver.get("https://www.instagram.com/accounts/login/?hl=en")
        # self.driver.get("https://instagram.com/accounts/login/")
        self.driver.execute_script('localStorage.clear();')	
	
        # convert unicode in instagram title to spaces for comparison
        titleString = ''.join([i if ord(i) < 128 else ' ' for i in self.driver.title])
		
        if (titleString.startswith("Login")):                 
            print("\n[+] Instagram Login Page loaded successfully [+]")
            try:
                instagramUsername = self.driver.find_element_by_xpath("//input[@name='username']")
            except:
                print(
                    "Instagram Login Page username field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
            instagramUsername.send_keys(username)
            try:
                instagramPassword = self.driver.find_element_by_xpath("//input[@name='password']")
            except:
                print(
                    "Instagram Login Page password field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
            instagramPassword.send_keys(password)
            try:
                #self.driver.find_element_by_xpath("//button[contains(.,'Log In')]").click()
                self.driver.find_element_by_tag_name('form').submit()
            except:            	
                print(
                    "Instagram Login Page login button seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")
            # self.driver.find_element_by_class_name("submit").click()
            # self.driver.find_element_by_css_selector("button.submit.btn.primary-btn").click()
            sleep(5)
            if (self.driver.title.encode('utf8', 'replace').startswith(bytes("Instagram", 'utf-8')) == True):
                print("[+] Instagram Login Success [+]\n")
                try:
                    # print("Closing \"Turn On Notifications\" message")
                    self.driver.find_element_by_class_name("aOOlW").click()
                    sleep(3)
                except:
                    # print("Closing Message Failed or did not exist")
                    pass
            else:
                print("[-] Instagram Login Failed [-]\n")
        # sleep(3600)
        else:
            print(
                "Instagram Login Page title field seems to have changed, please make an issue on: https://github.com/Greenwolf/social_mapper")

    def getInstagramProfiles(self, first_name, last_name, username, password):
        try:
            url = "https://www.instagram.com/"
            self.driver.get(url)
            sleep(3)
            try:
                # print("Closing \"Turn On Notifications\" message")
                self.driver.find_element_by_class_name("aOOlW").click()
                sleep(3)
            except:
                # print("Closing Message Failed or did not exist")
                pass
            # searchbar = self.driver.find_element_by_xpath("//body")
            # searchbar.send_keys(Keys.TAB)
            # searchbar = self.driver.find_element_by_class_name("_avvq0").click()
            picturelist = []
            try:
                searchbar = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
            except:
                # if cant find search bar try to relogin
                self.doLogin(username, password)
                self.driver.get(url)
                sleep(3)
                try:
                    searchbar = self.driver.find_element_by_xpath("//input[@placeholder='Search']")
                except:
                    print("Instagram Timeout Error, session has expired and attempts to reestablish have failed")
                    return picturelist
            sleep(1)
            full_name = first_name + " " + last_name
            searchbar.send_keys(full_name)
            sleep(1)
            searchresponse = self.driver.page_source.encode('utf-8')
            sleep(1)
            soupParser = BeautifulSoup(searchresponse, 'html.parser')

            # for element in soupParser.find_all('a', {'class': '_ndl3t'}):
            for element in soupParser.find_all('a', {'class': 'yCE8d'}):
                # print element
                link = element['href']
                try:
                    # profilepic = element.find('img')['src']
                    # print profilepic
                    # Errors with instagram https://github.com/stevenschobert/instafeed.js/issues/549

                    # Old code for getting a bigger instagram profile picture, doesnt work since March 23rd 2018
                    # profilepicwithsmallid = element.find('img')['src']
                    # if not "150x150" in profilepicwithsmallid:
                    #    continue
                    # profilepicbadurl = profilepicwithsmallid.replace('150x150', '600x600')
                    # profilepic = profilepicbadurl.split("/")[0] + "//" + profilepicbadurl.split("/")[2] + "/" + profilepicbadurl.split("/")[6] + "/" + profilepicbadurl.split("/")[7] + "/" + profilepicbadurl.split("/")[8]

                    # New code for getting instagram profile pic, if possible make it better with a bigger image, but may not be possible anymore
                    profilepic = element.find('img')['src']

                    picturelist.append(["https://instagram.com" + link, profilepic, 1.0])
                except:
                    # The find imgsrc fails on search items that arn't profiles so we catch and continue
                    continue

            return picturelist
        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno) + e)
            picturelist = []
            # print "Error"
            return picturelist

    def testdeletecookies(self):
        self.driver.delete_all_cookies()

    def kill(self):
        self.driver.quit()
