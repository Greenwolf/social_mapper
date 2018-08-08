from modules import facebookfinder
from modules import twitterfinder
from modules import instagramfinder
from modules import linkedinfinder
from modules import vkontaktefinder
from modules import weibofinder
from modules import doubanfinder
from modules import googleplusfinder
from shutil import copyfile
import facebook
import requests
import sys
import csv
import face_recognition
import urllib
import urllib2
import os
import codecs
import argparse
import shutil
import cookielib
import json
from datetime import datetime
from bs4 import BeautifulSoup
from django.utils import encoding



global linkedin_username
global linkedin_password
linkedin_username = ""
linkedin_password = ""
global facebook_username 
global facebook_password 
facebook_username = ""
facebook_password = ""
global twitter_username
global twitter_password
twitter_username = ""
twitter_password = ""
global instagram_username
global instagram_password
instagram_username = ""
instagram_password = ""
global google_username
global google_password
google_username = ""
google_password = ""
global vk_username
global vk_password
vk_username = "" # Can be mobile or email
vk_password = ""
global weibo_username
global weibo_password
weibo_username = "" # Can be mobile
weibo_password = ""
global douban_username
global douban_password
douban_username = ""
douban_password = ""


startTime = datetime.now()

class Person(object):
    first_name = ""
    last_name = ""
    full_name = ""
    person_image = ""
    person_imagelink = ""
    linkedin = ""
    linkedinimage = ""
    facebook = ""
    facebookimage = "" #higher quality but needs authentication to access 
    facebookcdnimage = "" #lower quality but not authentication, used for html output
    twitter = ""
    twitterimage = ""
    instagram = ""
    instagramimage = ""
    vk = ""
    vkimage = ""
    weibo = ""
    weiboimage = ""
    douban = ""
    doubanimage = ""
    googleplus = ""
    googleplusimage = ""
    def __init__(self, first_name, last_name, full_name, person_image):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = full_name
        self.person_image = person_image

class PotentialPerson(object):
    full_name = ""
    profile_link = ""
    image_link = ""
    def __init__(self, full_name, profile_link, image_link):
        self.full_name = full_name
        self.profile_link = profile_link
        self.image_link = image_link

def fill_facebook(peoplelist):
    FacebookfinderObject = facebookfinder.Facebookfinder(showbrowser)
    FacebookfinderObject.doLogin(facebook_username,facebook_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        if args.vv == True:
            print "Facebook Check %i/%i : %s" % (count,ammount,person.full_name)
        else:
            sys.stdout.write("\rFacebook Check %i/%i : %s                                " % (count,ammount,person.full_name))
            sys.stdout.flush()
        count = count + 1            
        #Testcode to mimic a session timeout
        #if count == 3: 
        #    print "triggered delete"
        #    FacebookfinderObject.testdeletecookies()
        if person.person_image:
            try:
                target_image = face_recognition.load_image_file(person.person_image)
                target_encoding = face_recognition.face_encodings(target_image)[0]
                profilelist = FacebookfinderObject.getFacebookProfiles(person.first_name, person.last_name,facebook_username,facebook_password)
            except:
                continue
        else:
            continue

        early_break = False
        updatedlist = []
        #for profilelink,distance in profilelist:
        for profilelink,profilepic,distance,cdnpicture in profilelist:
            try:
                os.remove("potential_target_image.jpg")
            except:
                pass
            if early_break:
                break
            #image_link = FacebookfinderObject.getProfilePicture(profilelink)
            image_link = profilepic
            #print profilelink
            #print image_link
            #print "----"
            cookies = FacebookfinderObject.getCookies()
            if image_link:  
                try: 
                    # Set fake user agent as facebook blocks python requests default user agent
                    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'}
                    # Get target image using requests, providing selenium cookies, and fake user agent
                    response = requests.get(image_link, cookies=cookies,headers=headers,stream=True)
                    with open('potential_target_image.jpg', 'wb') as out_file:
                        #facebook images are sent content encoded so need to decode them
                        response.raw.decode_content = True
                        shutil.copyfileobj(response.raw, out_file)
                    del response
                    potential_target_image = face_recognition.load_image_file("potential_target_image.jpg")
                    try: # try block for when an image has no faces
                        potential_target_encoding = face_recognition.face_encodings(potential_target_image)[0]
                    except:
                        continue
                    results = face_recognition.face_distance([target_encoding], potential_target_encoding)
                    for result in results:
                        #print profilelink + " + " + cdnpicture + " + " + image_link
                        #print result 
                        #print ""
                        # check here to do early break if using fast mode, otherwise if accurate set highest distance in array then do a check for highest afterwards 
                        if args.mode == "fast":
                            if result < threshold:
                                person.facebook = encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
                                person.facebookimage = encoding.smart_str(image_link, encoding='ascii', errors='ignore')
                                person.facebookcdnimage = encoding.smart_str(cdnpicture, encoding='ascii', errors='ignore')
                                if args.vv == True:
                                    print "\tMatch found: " + person.full_name
                                    print "\tFacebook: " + person.facebook
                                early_break = True
                                break
                        elif args.mode == "accurate":
                            #code for accurate mode here, check if result is higher than current distace (best match in photo with multiple people) and store highest for later comparison
                            if result < threshold:
                                #print "Adding to updated list"
                                #print distance
                                #print "Match over threshold: \n" + profilelink + "\n" + result
                                updatedlist.append([profilelink,image_link,result,cdnpicture])
                except Exception as e: 
                    print e
                    #print(e)
                    #print "Error getting image link, retrying login and getting fresh cookies"
                    #FacebookfinderObject.doLogin(facebook_username,facebook_password)
                    #cookies = FacebookfinderObject.getCookies()
                    continue
        # For accurate mode pull out largest distance and if its bigger than the threshold then its the most accurate result 
        if args.mode == "accurate":
            highestdistance=1.0
            bestprofilelink=""
            bestimagelink=""
            for profilelink,image_link,distance,cdnpicture in updatedlist:
                if distance < highestdistance:
                    highestdistance = distance
                    bestprofilelink = profilelink
                    bestimagelink = image_link
                    bestcdnpicture = cdnpicture
            if highestdistance < threshold:
                person.facebook = encoding.smart_str(bestprofilelink, encoding='ascii', errors='ignore')
                person.facebookimage = encoding.smart_str(bestimagelink, encoding='ascii', errors='ignore')
                person.facebookcdnimage = encoding.smart_str(bestcdnpicture, encoding='ascii', errors='ignore')
                if args.vv == True:
                    print "\tMatch found: " + person.full_name
                    print "\tFacebook: " + person.facebook
    try:               
        FacebookfinderObject.kill()
    except: 
        print "Error Killing Facebook Selenium instance"
    return peoplelist

def fill_twitter(peoplelist):
    TwitterfinderObject = twitterfinder.Twitterfinder(showbrowser)
    TwitterfinderObject.doLogin(twitter_username,twitter_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        if args.vv == True:
            print "Twitter Check %i/%i : %s" % (count,ammount,person.full_name)
        else:
            sys.stdout.write("\rTwitter Check %i/%i : %s                                " % (count,ammount,person.full_name))
            sys.stdout.flush()   
        count = count + 1         
        if person.person_image:
            try:
                target_image = face_recognition.load_image_file(person.person_image)
                target_encoding = face_recognition.face_encodings(target_image)[0]
                profilelist = TwitterfinderObject.getTwitterProfiles(person.first_name, person.last_name)
            except:
                continue
        else:
            continue

        early_break = False
        updatedlist = []
        for profilelink,profilepic,distance in profilelist:
            try:
                os.remove("potential_target_image.jpg")
            except:
                pass
            if early_break:
                break
            image_link = profilepic
            if image_link:   
                try: 
                    urllib.urlretrieve(image_link, "potential_target_image.jpg")
                    potential_target_image = face_recognition.load_image_file("potential_target_image.jpg")
                    try: # try block for when an image has no faces
                        potential_target_encoding = face_recognition.face_encodings(potential_target_image)[0]
                    except:
                        continue
                    results = face_recognition.face_distance([target_encoding], potential_target_encoding)
                    for result in results:
                        if args.mode == "fast":
                            if result < threshold:
                                person.twitter = encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
                                person.twitterimage = encoding.smart_str(image_link, encoding='ascii', errors='ignore')
                                if args.vv == True:
                                    print "\tMatch found: " + person.full_name
                                    print "\tTwitter: " + person.twitter
                                early_break = True
                                break
                        elif args.mode == "accurate":
                            if result < threshold:
                                updatedlist.append([profilelink,image_link,result])
                except:
                    continue
        if args.mode == "accurate":
            highestdistance=1.0
            bestprofilelink=""
            bestimagelink=""
            for profilelink,image_link,distance in updatedlist:
                if distance < highestdistance:
                    highestdistance = distance
                    bestprofilelink = profilelink
                    bestimagelink = image_link
            if highestdistance < threshold:
                person.twitter = encoding.smart_str(bestprofilelink, encoding='ascii', errors='ignore')
                person.twitterimage = encoding.smart_str(bestimagelink, encoding='ascii', errors='ignore')
                if args.vv == True:
                    print "\tMatch found: " + person.full_name
                    print "\tTwitter: " + person.twitter 
    try:
        TwitterfinderObject.kill()
    except: 
        print "Error Killing Twitter Selenium instance"
    return peoplelist

def fill_instagram(peoplelist):
    InstagramfinderObject = instagramfinder.Instagramfinder(showbrowser)
    InstagramfinderObject.doLogin(instagram_username,instagram_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        if args.vv == True:
            print "Instagram Check %i/%i : %s" % (count,ammount,person.full_name)
        else:
            sys.stdout.write("\rInstagram Check %i/%i : %s                                " % (count,ammount,person.full_name))
            sys.stdout.flush()  
        count = count + 1   
        #if count == 3: 
        #    print "triggered delete"
        #    InstagramfinderObject.testdeletecookies()       
        if person.person_image:
            try:
                target_image = face_recognition.load_image_file(person.person_image)
                target_encoding = face_recognition.face_encodings(target_image)[0]
                profilelist = InstagramfinderObject.getInstagramProfiles(person.first_name, person.last_name,instagram_username,instagram_password)
                #print "DEBUG"
                #print profilelist
                #print ""
            except:
                continue
        else:
            continue

        early_break = False
        #print "DEBUG: " + person.full_name
        updatedlist = []
        for profilelink,profilepic,distance in profilelist:
            try:
                os.remove("potential_target_image.jpg")
            except:
                pass
            if early_break:
                break
            image_link = profilepic
            if image_link:   
                try: 
                    urllib.urlretrieve(image_link, "potential_target_image.jpg")
                    potential_target_image = face_recognition.load_image_file("potential_target_image.jpg")
                    try: # try block for when an image has no faces
                        potential_target_encoding = face_recognition.face_encodings(potential_target_image)[0]
                    except:
                        continue     
                    results = face_recognition.face_distance([target_encoding], potential_target_encoding)
                    for result in results:
                        if args.mode == "fast":
                            if result < threshold:
                                person.instagram = encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
                                person.instagramimage = encoding.smart_str(image_link, encoding='ascii', errors='ignore')
                                if args.vv == True:
                                    print "\tMatch found: " + person.full_name
                                    print "\tInstagram: " + person.instagram
                                early_break = True
                                break
                        elif args.mode == "accurate":
                            if result < threshold:
                                #distance=result
                                updatedlist.append([profilelink,image_link,result])
                except Exception as e: 
                    print "ERROR"
                    print e
        if args.mode == "accurate":
            highestdistance=1.0
            bestprofilelink=""
            bestimagelink=""
            for profilelink,image_link,distance in updatedlist:
                if distance < highestdistance:
                    highestdistance = distance
                    bestprofilelink = profilelink
                    bestimagelink = image_link
            if highestdistance < threshold:
                person.instagram = encoding.smart_str(bestprofilelink, encoding='ascii', errors='ignore')
                person.instagramimage = encoding.smart_str(bestimagelink, encoding='ascii', errors='ignore')
                if args.vv == True:
                    print "\tMatch found: " + person.full_name
                    print "\tInstagram: " + person.instagram
    try:
        InstagramfinderObject.kill()
    except: 
        print "Error Killing Instagram Selenium instance"
    return peoplelist

def fill_linkedin(peoplelist):
    LinkedinfinderObject = linkedinfinder.Linkedinfinder(showbrowser)
    LinkedinfinderObject.doLogin(linkedin_username,linkedin_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        if args.vv == True:
            print "LinkedIn Check %i/%i : %s" % (count,ammount,person.full_name)
        else:
            sys.stdout.write("\rLinkedIn Check %i/%i : %s                                " % (count,ammount,person.full_name))
            sys.stdout.flush()     
        count = count + 1
        #if count == 3: 
            #print "triggered delete"
        #    LinkedinfinderObject.testdeletecookies()       
        if person.person_image:
            try:
                target_image = face_recognition.load_image_file(person.person_image)
                target_encoding = face_recognition.face_encodings(target_image)[0]
                profilelist = LinkedinfinderObject.getLinkedinProfiles(person.first_name, person.last_name,linkedin_username,linkedin_password)
            except:
                continue
        else:
            continue

        early_break = False
        #print "DEBUG: " + person.full_name
        updatedlist = []
        for profilelink,profilepic,distance in profilelist:
            try:
                os.remove("potential_target_image.jpg")
            except:
                pass
            if early_break:
                break
            image_link = profilepic
            if image_link:   
                try: 
                    urllib.urlretrieve(image_link, "potential_target_image.jpg")
                    potential_target_image = face_recognition.load_image_file("potential_target_image.jpg")
                    try: # try block for when an image has no faces
                        potential_target_encoding = face_recognition.face_encodings(potential_target_image)[0]
                    except:
                        continue     
                    results = face_recognition.face_distance([target_encoding], potential_target_encoding)
                    for result in results:
                        if args.mode == "fast":
                            if result < threshold:
                                person.linkedin = encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
                                person.linkedinimage = encoding.smart_str(image_link, encoding='ascii', errors='ignore')
                                if args.vv == True:
                                    print "\tMatch found: " + person.full_name
                                    print "\tLinkedIn: " + person.linkedin
                                early_break = True
                                break
                        elif args.mode == "accurate":
                            if result < threshold:
                                #distance=result
                                updatedlist.append([profilelink,image_link,result])
                except Exception as e: 
                    print e
        if args.mode == "accurate":
            highestdistance=1.0
            bestprofilelink=""
            bestimagelink=""
            for profilelink,image_link,distance in updatedlist:
                if distance < highestdistance:
                    highestdistance = distance
                    bestprofilelink = profilelink
                    bestimagelink = image_link
            if highestdistance < threshold:
                person.linkedin = encoding.smart_str(bestprofilelink, encoding='ascii', errors='ignore')
                person.linkedinimage = encoding.smart_str(bestimagelink, encoding='ascii', errors='ignore')
                if args.vv == True:
                    print "\tMatch found: " + person.full_name
                    print "\tLinkedIn: " + person.linkedin    
    try:
        LinkedinfinderObject.kill()
    except: 
        print "Error Killing LinkedIn Selenium instance"
    return peoplelist

def fill_googleplus(peoplelist):
    GooglePlusfinderObject = googleplusfinder.GooglePlusfinder(showbrowser)
    GooglePlusfinderObject.doLogin(google_username,google_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        if args.vv == True:
            print "GooglePlus Check %i/%i : %s" % (count,ammount,person.full_name)
        else:
            sys.stdout.write("\rGooglePlus Check %i/%i : %s                                " % (count,ammount,person.full_name))
            sys.stdout.flush()
        count = count + 1         
        if person.person_image:
            try:
                target_image = face_recognition.load_image_file(person.person_image)
                target_encoding = face_recognition.face_encodings(target_image)[0]
                profilelist = GooglePlusfinderObject.getGooglePlusProfiles(person.first_name, person.last_name)
            except:
                continue
        else:
            continue

        early_break = False
        #print "DEBUG: " + person.full_name
        updatedlist = []
        for profilelink,profilepic,distance in profilelist:
            try:
                os.remove("potential_target_image.jpg")
            except:
                pass
            if early_break:
                break
            image_link = profilepic
            if image_link:   
                try: 
                    urllib.urlretrieve(image_link, "potential_target_image.jpg")
                    potential_target_image = face_recognition.load_image_file("potential_target_image.jpg")
                    try: # try block for when an image has no faces
                        potential_target_encoding = face_recognition.face_encodings(potential_target_image)[0]
                    except:
                        continue      
                    results = face_recognition.face_distance([target_encoding], potential_target_encoding)
                    for result in results:
                        if args.mode == "fast":
                            if result < threshold:
                                person.googleplus = encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
                                person.googleplusimage = encoding.smart_str(image_link, encoding='ascii', errors='ignore')
                                if args.vv == True:
                                    print "\tMatch found: " + person.full_name
                                    print "\tGoogle Plus: " + person.googleplus
                                early_break = True
                                break
                        elif args.mode == "accurate":
                            if result < threshold:
                                #distance=result
                                updatedlist.append([profilelink,image_link,result])
                except Exception as e: 
                    print e
        if args.mode == "accurate":
            highestdistance=1.0
            bestprofilelink=""
            bestimagelink=""
            for profilelink,image_link,distance in updatedlist:
                if distance < highestdistance:
                    highestdistance = distance
                    bestprofilelink = profilelink
                    bestimagelink = image_link
            if highestdistance < threshold:
                person.googleplus = encoding.smart_str(bestprofilelink, encoding='ascii', errors='ignore')
                person.googleplusimage = encoding.smart_str(bestimagelink, encoding='ascii', errors='ignore')
                if args.vv == True:
                    print "\tMatch found: " + person.full_name
                    print "\tGoogle Plus: " + person.googleplus     
    try:
        GooglePlusfinderObject.kill()
    except: 
        print "Error Killing GooglePlus Selenium instance"
    return peoplelist

def fill_vkontakte(peoplelist):
    VkontaktefinderObject = vkontaktefinder.Vkontaktefinder(showbrowser)
    VkontaktefinderObject.doLogin(vk_username,vk_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        if args.vv == True:
            print "VKontakte Check %i/%i : %s" % (count,ammount,person.full_name)
        else:
            sys.stdout.write("\rVKontakte Check %i/%i : %s                                " % (count,ammount,person.full_name))
            sys.stdout.flush()  
        count = count + 1          
        if person.person_image:
            try:
                target_image = face_recognition.load_image_file(person.person_image)
                target_encoding = face_recognition.face_encodings(target_image)[0]
                profilelist = VkontaktefinderObject.getVkontakteProfiles(person.first_name, person.last_name)
            except:
                continue
        else:
            continue

        early_break = False
        #print "DEBUG: " + person.full_name
        updatedlist = []
        for profilelink,profilepic,distance in profilelist:
            try:
                os.remove("potential_target_image.jpg")
            except:
                pass
            if early_break:
                break
            image_link = profilepic
            if image_link:   
                try: 
                    urllib.urlretrieve(image_link, "potential_target_image.jpg")
                    potential_target_image = face_recognition.load_image_file("potential_target_image.jpg")
                    try: # try block for when an image has no faces
                        potential_target_encoding = face_recognition.face_encodings(potential_target_image)[0]
                    except:
                        continue     
                    results = face_recognition.face_distance([target_encoding], potential_target_encoding)
                    for result in results:
                        if args.mode == "fast":
                            if result < threshold:
                                person.vk = encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
                                person.vkimage = encoding.smart_str(image_link, encoding='ascii', errors='ignore')
                                if args.vv == True:
                                    print "\tnMatch found: " + person.full_name
                                    print "\tVkontakte: " + person.vk
                                early_break = True
                                break
                        elif args.mode == "accurate":
                            if result < threshold:
                                #distance=result
                                updatedlist.append([profilelink,image_link,result])
                except Exception as e: 
                    print e
        if args.mode == "accurate":
            highestdistance=1.0
            bestprofilelink=""
            bestimagelink=""
            for profilelink,image_link,distance in updatedlist:
                if distance < highestdistance:
                    highestdistance = distance
                    bestprofilelink = profilelink
                    bestimagelink = image_link
            if highestdistance < threshold:
                person.vk = encoding.smart_str(bestprofilelink, encoding='ascii', errors='ignore')
                person.vkimage = encoding.smart_str(bestimagelink, encoding='ascii', errors='ignore')
                if args.vv == True:
                    print "\tMatch found: " + person.full_name
                    print "\tVkontakte: " + person.vk   
    try:
        VkontaktefinderObject.kill()
    except: 
        print "Error Killing VKontakte Selenium instance"
    return peoplelist

def fill_weibo(peoplelist):
    WeibofinderObject = weibofinder.Weibofinder(showbrowser)
    WeibofinderObject.doLogin(weibo_username,weibo_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        if args.vv == True:
            print "Weibo Check %i/%i : %s" % (count,ammount,person.full_name)
        else:
            sys.stdout.write("\rWeibo Check %i/%i : %s                                " % (count,ammount,person.full_name))
            sys.stdout.flush() 
        count = count + 1           
        if person.person_image:
            try:
                target_image = face_recognition.load_image_file(person.person_image)
                target_encoding = face_recognition.face_encodings(target_image)[0]
                profilelist = WeibofinderObject.getWeiboProfiles(person.first_name, person.last_name)
            except:
                continue
        else:
            continue

        early_break = False
        #print "DEBUG: " + person.full_name
        updatedlist = []
        for profilelink,profilepic,distance in profilelist:
            try:
                os.remove("potential_target_image.jpg")
            except:
                pass
            if early_break:
                break
            image_link = profilepic
            if image_link:   
                try: 
                    urllib.urlretrieve(image_link, "potential_target_image.jpg")
                    potential_target_image = face_recognition.load_image_file("potential_target_image.jpg")
                    try: # try block for when an image has no faces
                        potential_target_encoding = face_recognition.face_encodings(potential_target_image)[0]
                    except:
                        continue       
                    results = face_recognition.face_distance([target_encoding], potential_target_encoding)
                    for result in results:
                        if args.mode == "fast":
                            if result < threshold:
                                person.weibo =  encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
                                person.weiboimage =  encoding.smart_str(image_link, encoding='ascii', errors='ignore')
                                if args.vv == True:
                                    print "\tMatch found: " + person.full_name
                                    print "\tWeibo: " + person.weibo
                                early_break = True
                                break
                        elif args.mode == "accurate":
                            if result < threshold:
                                #distance=result
                                updatedlist.append([profilelink,image_link,result])
                except Exception as e: 
                    print e
        if args.mode == "accurate":
            highestdistance=1.0
            bestprofilelink=""
            bestimagelink=""
            for profilelink,image_link,distance in updatedlist:
                if distance < highestdistance:
                    highestdistance = distance
                    bestprofilelink = profilelink
                    bestimagelink = image_link
            if highestdistance < threshold:
                person.weibo =  encoding.smart_str(bestprofilelink, encoding='ascii', errors='ignore')
                person.weiboimage =  encoding.smart_str(bestimagelink, encoding='ascii', errors='ignore')
                if args.vv == True:
                    print "\tMatch found: " + person.full_name
                    print "\tWeibo: " + person.weibo   
    try:
        WeibofinderObject.kill()
    except: 
        print "Error Killing Weibo Selenium instance"
    return peoplelist

def fill_douban(peoplelist):
    DoubanfinderObject = doubanfinder.Doubanfinder(showbrowser)
    DoubanfinderObject.doLogin(douban_username,douban_password)

    count=1
    ammount=len(peoplelist)                      
    for person in peoplelist:
        if args.vv == True:
            print "Douban Check %i/%i : %s" % (count,ammount,person.full_name)
        else:
            sys.stdout.write("\rDouban Check %i/%i : %s                                " % (count,ammount,person.full_name))
            sys.stdout.flush()
        count = count + 1          
        if person.person_image:
            try:
                target_image = face_recognition.load_image_file(person.person_image)
                target_encoding = face_recognition.face_encodings(target_image)[0]
                profilelist = DoubanfinderObject.getDoubanProfiles(person.first_name, person.last_name)
            except:
                continue
        else:
            continue

        early_break = False
        #print "DEBUG: " + person.full_name
        updatedlist = []
        for profilelink,profilepic,distance in profilelist:
            try:
                os.remove("potential_target_image.jpg")
            except:
                pass
            if early_break:
                break
            image_link = profilepic
            if image_link:   
                try: 
                    urllib.urlretrieve(image_link, "potential_target_image.jpg")
                    potential_target_image = face_recognition.load_image_file("potential_target_image.jpg")
                    try: # try block for when an image has no faces
                        potential_target_encoding = face_recognition.face_encodings(potential_target_image)[0]
                    except:
                        continue       
                    results = face_recognition.face_distance([target_encoding], potential_target_encoding)
                    for result in results:
                        if args.mode == "fast":
                            if result < threshold:
                                person.douban =  encoding.smart_str(profilelink, encoding='ascii', errors='ignore')
                                person.doubanimage =  encoding.smart_str(image_link, encoding='ascii', errors='ignore')
                                if args.vv == True:
                                    print "\tMatch found: " + person.full_name
                                    print "\tDouban: " + person.douban
                                early_break = True
                                break
                        elif args.mode == "accurate":
                            if result < threshold:
                                #distance=result
                                updatedlist.append([profilelink,image_link,result])
                except Exception as e: 
                    print e
        if args.mode == "accurate":
            highestdistance=1.0
            bestprofilelink=""
            bestimagelink=""
            for profilelink,image_link,distance in updatedlist:
                if distance < highestdistance:
                    highestdistance = distance
                    bestprofilelink = profilelink
                    bestimagelink = image_link
            if highestdistance < threshold:
                person.douban =  encoding.smart_str(bestprofilelink, encoding='ascii', errors='ignore')
                person.doubanimage =  encoding.smart_str(bestimagelink, encoding='ascii', errors='ignore')
                if args.vv == True:
                    print "\tMatch found: " + person.full_name
                    print "\tDouban: " + person.douban   
    try:
        DoubanfinderObject.kill()
    except: 
        print "Error Killing Douban Selenium instance"
    return peoplelist

#Login function for linkedin for company browsing (Credits to LinkedInt from MDSec)
def login():
    cookie_filename = "cookies.txt"
    cookiejar = cookielib.MozillaCookieJar(cookie_filename)
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler(),urllib2.HTTPHandler(debuglevel=0),urllib2.HTTPSHandler(debuglevel=0),urllib2.HTTPCookieProcessor(cookiejar))
    page = loadPage(opener, "https://www.linkedin.com/")
    parse = BeautifulSoup(page, "html.parser")
    csrf = parse.find(id="loginCsrfParam-login")['value']
    login_data = urllib.urlencode({'session_key': linkedin_username, 'session_password': linkedin_password, 'loginCsrfParam': csrf})
    page = loadPage(opener,"https://www.linkedin.com/uas/login-submit", login_data)
    parse = BeautifulSoup(page, "html.parser")
    cookie = ""
    try:
        cookie = cookiejar._cookies['.www.linkedin.com']['/']['li_at'].value
    except:
        sys.exit(0)
    cookiejar.save()
    os.remove(cookie_filename)
    return cookie

def authenticate():
    try:
        a = login()
        print a
        session = a
        if len(session) == 0:
            sys.exit("[!] Unable to login to LinkedIn.com")
        print "[*] Obtained new session: %s" % session
        cookies = dict(li_at=session)
    except Exception, e:
        sys.exit("[!] Could not authenticate to linkedin. %s" % e)
    return cookies

def loadPage(client, url, data=None):
    try:
        response = client.open(url)
    except:
        print "[!] Cannot load main LinkedIn page"
    try:
        if data is not None:
            response = client.open(url, data)
        else:
            response = client.open(url)
        return ''.join(response.readlines())
    except:
        sys.exit(0)

#Setup Argument parser to print help and lock down options
parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Social Mapper by Jacob Wilkin(Greenwolf)',
        usage='%(prog)s -f <format> -i <input> -m <mode> -t <threshold> <options>')
parser.add_argument('-v', '--version', action='version',
    version='%(prog)s 0.1.0 : Social Mapper by Greenwolf (Github Link Here)')
parser.add_argument('-vv', '--verbose', action='store_true',dest='vv',help='Verbose Mode')
parser.add_argument('-f', '--format',action='store', dest='format',required=True,choices=set(("csv","imagefolder","company","socialmapper")),
    help='Specify if the input file is either a \'company\',a \'csv\',a \'imagefolder\' or a social mapper html file to resume')
parser.add_argument('-i', '--input',action='store', dest='input',required=True,
    help='The name of the csv file, input folder or company name to use as input')
parser.add_argument('-m', '--mode',action='store', dest='mode',required=True,choices=set(("accurate","fast")),
    help='Selects the mode either accurate or fast, fast will report the first match over the threshold while accurate will check for the highest match over the threshold')
parser.add_argument('-t', '--threshold',action='store', dest='thresholdinput',required=False,choices=set(("loose","standard","strict","superstrict")),
    help='The strictness level for image matching, default is standard but can be specified to loose,standard,strict or superstrict')
parser.add_argument('-e', '--email',action='store', dest='email',required=False,
    help='Provide an email format to trigger phishing list generation output, should follow a convention such as "<first><last><f><l>@domain.com"')
parser.add_argument('-cid', '--companyid',action='store', dest='companyid',required=False,
    help='Provide an optional company id, for use with \'-f company\' only')

parser.add_argument('-s', '--showbrowser',action='store_true',dest='showbrowser',help='If flag is set then browser will be visible')

parser.add_argument('-a', '--all',action='store_true',dest='a',help='Flag to check all social media sites')
parser.add_argument('-fb', '--facebook',action='store_true',dest='fb',help='Flag to check Facebook')
parser.add_argument('-tw', '--twitter',action='store_true',dest='tw',help='Flag to check Twitter')
parser.add_argument('-ig', '--instagram',action='store_true',dest='ig',help='Flag to check Instagram')
parser.add_argument('-li', '--linkedin',action='store_true',dest='li',help='Flag to check LinkedIn - Automatic with \'company\' input type')
parser.add_argument('-gp', '--googleplus',action='store_true',dest='gp',help='Flag to check Google Plus')
parser.add_argument('-vk', '--vkontakte',action='store_true',dest='vk',help='Flag to check the Russian VK VKontakte Site')
parser.add_argument('-wb', '--weibo',action='store_true',dest='wb',help='Flag to check the Chinese Weibo Site')
parser.add_argument('-db', '--douban',action='store_true',dest='db',help='Flag to check the Chinese Douban Site')

args = parser.parse_args()

if not (args.a or args.fb or args.tw or args.ig or args.li or args.gp or args.vk or args.wb or args.db):
    parser.error('No sites specified requested, add -a for all, or a combination of the sites you want to check using a mix of -fb -tw -ig -li')

#Set up face matching threshold
threshold = 0.6
try:
    if args.thresholdinput == "superstrict":
        threshold = 0.4
    if args.thresholdinput == "strict":
        threshold = 0.5 
    if args.thresholdinput == "standard":
        threshold = 0.6
    if args.thresholdinput == "loose":
        threshold = 0.7
except:
    pass

if args.showbrowser:
    showbrowser=True
else:
    showbrowser=False

exit=True
#remove targets dir for remaking
if os.path.exists('temp-targets'):
    shutil.rmtree('temp-targets')
#people list to hold people in memory
peoplelist = []

# Fill people list from document with just name + image link
if args.format == "csv":
    exit=False
    file = open(args.input, 'rb')
    data = file.read()
    file.close()
    try:
        os.remove('temp.csv')
    except OSError:
        pass
    tempcsv = open('temp.csv', 'wb')
    tempcsv.write(data.replace('\x00',''))
    tempcsv.close()
    if not os.path.exists('temp-targets'):
        os.makedirs('temp-targets')
    filereader = csv.reader(open('temp.csv', 'rb'), delimiter=",")
    for full_name, person_image in filereader:
        full_name = encoding.smart_str(full_name, encoding='ascii', errors='ignore')
        person_image = encoding.smart_str(person_image, encoding='ascii', errors='ignore')
        #print person_image
        urllib.urlretrieve(person_image, "temp-targets/" + full_name + ".jpg")
        first_name = full_name.split(" ")[0]
        last_name = full_name.split(" ",1)[1]
        person = Person(first_name, last_name, full_name, "temp-targets/" + full_name + ".jpg")
        person.person_imagelink = person_image
        peoplelist.append(person)

#remove this when fixed downloading
#sys.exit(1)     

# Parse image folder full of images and names into social_mapper
if args.format == "imagefolder":
    if not args.input.endswith("/"):
        args.input = args.input + "/"
    exit=False
    for filename in os.listdir(args.input):
        if filename.endswith(".jpg") or filename.endswith(".png")or filename.endswith(".jpeg"):
            full_name = filename.split(".")[0]
            first_name = full_name.split(" ")[0]
            try:
                last_name = full_name.split(" ")[1]
            except:
                last_name = ""
            first_name = encoding.smart_str(first_name, encoding='ascii', errors='ignore')
            last_name = encoding.smart_str(last_name, encoding='ascii', errors='ignore')
            full_name = encoding.smart_str(full_name, encoding='ascii', errors='ignore')
            person = Person(first_name, last_name, full_name, args.input + filename)
            person.person_imagelink = args.input + filename
            peoplelist.append(person)

# Get targets from linkedin company search
if args.format == "company":
    exit=False
    if not os.path.exists('temp-targets'):
        os.makedirs('temp-targets')
    cookies = authenticate() # perform authentication
    companyid = 0
    if args.companyid is not None: # Dont find company id, use provided id from -cid or --companyid flag
        print "Using supplied company Id: %s" % args.companyid
        companyid = args.companyid
    else:
        #code to get company ID based on name 
        companyid = 0
        url = "https://www.linkedin.com/voyager/api/typeahead/hits?q=blended&query=%s" % args.input
        headers = {'Csrf-Token':'ajax:0397788525211216808', 'X-RestLi-Protocol-Version':'2.0.0'}
        cookies['JSESSIONID'] = 'ajax:0397788525211216808'
        r = requests.get(url, cookies=cookies, headers=headers)
        content = json.loads(r.text)
        firstID = 0
        for i in range(0,len(content['elements'])):
            try:
                companyid = content['elements'][i]['hitInfo']['com.linkedin.voyager.typeahead.TypeaheadCompany']['id']
                if firstID == 0:
                    firstID = companyid
                print "[Notice] Found company ID: %s" % companyid
            except:
                continue
        companyid = firstID
        if companyid == 0:
            print "[WARNING] No valid company ID found in auto, please restart and find your own"
            sys.exit(1)
    print "[*] Using company ID: %s" % companyid

    url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&origin=OTHER&q=guided&start=0" % (companyid)
    headers = {'Csrf-Token':'ajax:0397788525211216808', 'X-RestLi-Protocol-Version':'2.0.0'}
    cookies['JSESSIONID'] = 'ajax:0397788525211216808'
    r = requests.get(url, cookies=cookies, headers=headers)
    content = json.loads(r.text)
    data_total = content['elements'][0]['total']

    # Calculate pages off final results at 40 results/page
    pages = data_total / 40
    if pages == 0:
        pages = 1
    if data_total % 40 == 0:
        # Becuase we count 0... Subtract a page if there are no left over results on the last page
        pages = pages - 1 
    if pages == 0: 
        print "[!] Try to use quotes in the search name"
        sys.exit(0)

    print "[*] %i Results Found" % data_total
    if data_total > 1000:
        pages = 25
        print "[*] LinkedIn only allows 1000 results. Refine keywords to capture all data"
    print "[*] Fetching %i Pages" % pages
    print
    companyname = args.input.strip("\"")
    for p in range(pages):
        url = "https://www.linkedin.com/voyager/api/search/cluster?count=40&guides=List(v->PEOPLE,facetCurrentCompany->%s)&origin=OTHER&q=guided&start=%i" % (companyid, p*40)
        r = requests.get(url, cookies=cookies, headers=headers)
        content = r.text.encode('UTF-8')
        content = json.loads(content)
        #print "[*] Fetching page %i with %i results for %s" % ((p),len(content['elements'][0]['elements']),companyname)
        sys.stdout.write("\r[*] Fetching page %i/%i with %i results for %s" % ((p),pages,len(content['elements'][0]['elements']),companyname))
        sys.stdout.flush()
        # code to get users, for each user with a picture create a person
        for c in content['elements'][0]['elements']:
            if 'com.linkedin.voyager.search.SearchProfile' in c['hitInfo'] and c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['headless'] == False:
                try:
                    # get the link to profile pic, link to linkedin profile page, and their full name
                    #person_image = "https://media.licdn.com/mpr/mpr/shrinknp_400_400%s" % c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.voyager.common.MediaProcessorImage']['id']
                    first_name = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['firstName']
                    first_name = encoding.smart_str(first_name, encoding='ascii', errors='ignore')
                    first_name = first_name.lower()
                    last_name = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['lastName']
                    last_name = encoding.smart_str(last_name, encoding='ascii', errors='ignore')
                    last_name = last_name.lower()
                    # Around 30% of people keep putting Certs in last name, so strip these out. 
                    last_name = last_name.split(' ',1)[0]
                    full_name = first_name + " " + last_name
                    #full_name = re.sub("[^a-zA-Z ]+", "", full_name)

                    rooturl = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.common.VectorImage']['rootUrl']
                    artifact = c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['picture']['com.linkedin.common.VectorImage']['artifacts'][3]['fileIdentifyingUrlPathSegment']
                    person_image = rooturl + artifact
                    person_image = encoding.smart_str(person_image, encoding='ascii', errors='ignore')
                    linkedin = "https://www.linkedin.com/in/%s" % c['hitInfo']['com.linkedin.voyager.search.SearchProfile']['miniProfile']['publicIdentifier']
                    linkedin = encoding.smart_str(linkedin, encoding='ascii', errors='ignore')
                    urllib.urlretrieve(person_image, "temp-targets/" + full_name + ".jpg")
                    person = Person(first_name, last_name, full_name, "temp-targets/" + full_name + ".jpg")
                    person.person_imagelink = person_image
                    person.linkedin = linkedin
                    person.linkedinimage = person_image
                    peoplelist.append(person)
                    #print person.linkedin
                    #print person_image
                except Exception, e:
                    # This triggers when a profile doesn't have an image associated with it
                    continue

# To continue a social mapper run for additional sites. 
if args.format == "socialmapper":
    if args.a == True:
        print "This option is for adding additional sites to a social mapper report\nFeed in a social mapper html file thats only been partially run, for example:\nFirst run(LinkedIn,Facebook,Twitter): python social_mapper -f company -i \"SpiderLabs\" -m fast -t standard -li -fb -tw\n Second run(adding Instagram and Google Plus): python social_mapper -f socialmapper -i SpiderLabs-social-mapper.html -m fast -t standard -ig -gp"
        sys.exit(1)
    exit=False
    try:
        os.remove('backup.html')
    except OSError:
        pass
    if not os.path.exists('temp-targets'):
        os.makedirs('temp-targets')
    copyfile(args.input,'SM-Results/backup.html')
    print "Backup of original report created: 'SM-Results/backup.html'"

    f = open(args.input)
    soup = BeautifulSoup(f, 'html.parser')
    f.close()

    tbodylist = soup.findAll("tbody")

    for personhtml in tbodylist:
        person_image = encoding.smart_str(personhtml.findAll("td")[0].string, encoding='ascii', errors='ignore').replace(";","")
        full_name = encoding.smart_str(personhtml.findAll("td")[1].string, encoding='ascii', errors='ignore')
        first_name = full_name.split(" ")[0]
        last_name = full_name.split(" ",1)[1]
        urllib.urlretrieve(person_image, "temp-targets/" + full_name + ".jpg")
        person = Person(first_name, last_name, full_name, "temp-targets/" + full_name + ".jpg")
        person.person_imagelink = person_image
        person.linkedin = encoding.smart_str(personhtml.findAll("td")[2].find("a")['href'], encoding='ascii', errors='ignore').replace(";","")
        person.linkedinimage = encoding.smart_str(personhtml.findAll("td")[2].find("img")['src'], encoding='ascii', errors='ignore').replace(";","")
        person.facebook = encoding.smart_str(personhtml.findAll("td")[3].find("a")['href'], encoding='ascii', errors='ignore').replace(";","")
        person.facebookimage = encoding.smart_str(personhtml.findAll("td")[3].find("img")['src'], encoding='ascii', errors='ignore').replace(";","")
        person.facebookcdnimage = encoding.smart_str(personhtml.findAll("td")[3].find("img")['src'], encoding='ascii', errors='ignore').replace(";","")
        person.twitter = encoding.smart_str(personhtml.findAll("td")[4].find("a")['href'], encoding='ascii', errors='ignore').replace(";","")
        person.twitterimage = encoding.smart_str(personhtml.findAll("td")[4].find("img")['src'], encoding='ascii', errors='ignore').replace(";","")
        person.instagram = encoding.smart_str(personhtml.findAll("td")[5].find("a")['href'], encoding='ascii', errors='ignore').replace(";","")
        person.instagramimage = encoding.smart_str(personhtml.findAll("td")[5].find("img")['src'], encoding='ascii', errors='ignore').replace(";","")
        person.googleplus = encoding.smart_str(personhtml.findAll("td")[6].find("a")['href'], encoding='ascii', errors='ignore').replace(";","")
        person.googleplusimage = encoding.smart_str(personhtml.findAll("td")[6].find("img")['src'], encoding='ascii', errors='ignore').replace(";","")
        person.vk = encoding.smart_str(personhtml.findAll("td")[7].find("a")['href'], encoding='ascii', errors='ignore').replace(";","")
        person.vkimage = encoding.smart_str(personhtml.findAll("td")[7].find("img")['src'], encoding='ascii', errors='ignore').replace(";","")
        person.weibo = encoding.smart_str(personhtml.findAll("td")[8].find("a")['href'], encoding='ascii', errors='ignore').replace(";","")
        person.weiboimage = encoding.smart_str(personhtml.findAll("td")[8].find("img")['src'], encoding='ascii', errors='ignore').replace(";","")
        person.douban = encoding.smart_str(personhtml.findAll("td")[9].find("a")['href'], encoding='ascii', errors='ignore').replace(";","")
        person.doubanimage = encoding.smart_str(personhtml.findAll("td")[9].find("img")['src'], encoding='ascii', errors='ignore').replace(";","")
        peoplelist.append(person)

if exit:
    print "Input Error, check options relating to format and input"
    sys.exit(1)

#Pass peoplelist to modules for filling out
if args.a == True or args.fb == True:
    if not (facebook_username == "" or facebook_password == ""):
        try:
            peoplelist = fill_facebook(peoplelist)
        except Exception, e:
            print "[-] Error Filling out Facebook Profiles [-]"
            print e
            print "[-]"
    else:
        print "Please provide Facebook Login Credentials in the social_mapper.py file"
if args.a == True or args.tw == True:
    if not (twitter_username == "" or twitter_password == ""):
        peoplelist = fill_twitter(peoplelist)
    else:
        print "Please provide Twitter Login Credentials in the social_mapper.py file"
if args.a == True or args.ig == True:
    if not (instagram_username == "" or instagram_password == ""):
        peoplelist = fill_instagram(peoplelist)
    else:
        print "Please provide Instagram Login Credentials in the social_mapper.py file"
if not args.format == "linkedint" and not args.format == "company":
    if args.a == True or args.li == True:
        if not (linkedin_username == "" or linkedin_password == ""):
            peoplelist = fill_linkedin(peoplelist)
        else:
            print "Please provide LinkedIn Login Credentials in the social_mapper.py file"
if args.a == True or args.gp == True:
    if not (google_username == "" or google_password == ""):
        peoplelist = fill_googleplus(peoplelist)
    else:
        print "Please provide Google Login Credentials in the social_mapper.py file"
if args.a == True or args.vk == True:
    if not (vk_username == "" or vk_password == ""):
        peoplelist = fill_vkontakte(peoplelist)
    else:
        print "Please provide VK (VKontakte) Login Credentials in the social_mapper.py file"
if args.a == True or args.wb == True:
    if not (weibo_username == "" or weibo_password == ""):
        peoplelist = fill_weibo(peoplelist)
    else:
        print "Please provide Weibo Login Credentials in the social_mapper.py file"
if args.a == True or args.db == True:
    if not (douban_username == "" or douban_password == ""):
        peoplelist = fill_douban(peoplelist)
    else:
        print "Please provide Douban Login Credentials in the social_mapper.py file"

#Write out updated people list to a csv file along with other output if 
csv = []

if not os.path.exists("SM-Results"):
    os.makedirs("SM-Results")

outputfilename = "SM-Results/" + args.input.replace("\"","").replace("/","-") + "-social-mapper.csv"
phishingoutputfilename = "SM-Results/" + args.input.replace("\"","").replace("/","-")
if args.format == "imagefolder":
    outputfilename = "SM-Results/results-social-mapper.csv"
    phishingoutputfilename = "SM-Results/results"
filewriter = open(outputfilename.format(outputfilename), 'wb')
titlestring = "Full Name,"
if args.a == True or args.li == True or args.format == "socialmapper":
        titlestring = titlestring + "LinkedIn,"
        if args.email is not None:
            phishingoutputfilenamelinkedin=phishingoutputfilename+"-linkedin.csv"
            filewriterlinkedin = open(phishingoutputfilenamelinkedin.format(phishingoutputfilenamelinkedin), 'wb')
if args.a == True or args.fb == True or args.format == "socialmapper":
        titlestring = titlestring + "Facebook,"
        if args.email is not None:
            phishingoutputfilenamefacebook=phishingoutputfilename+"-facebook.csv"
            filewriterfacebook = open(phishingoutputfilenamefacebook.format(phishingoutputfilenamefacebook), 'wb')
if args.a == True or args.tw == True or args.format == "socialmapper":
        titlestring = titlestring + "Twitter,"
        if args.email is not None:
            phishingoutputfilenametwitter=phishingoutputfilename+"-twitter.csv"
            filewritertwitter = open(phishingoutputfilenametwitter.format(phishingoutputfilenametwitter), 'wb')
if args.a == True or args.ig == True or args.format == "socialmapper":
        titlestring = titlestring + "Instagram,"
        if args.email is not None:
            phishingoutputfilenameinstagram=phishingoutputfilename+"-instagram.csv"
            filewriterinstagram = open(phishingoutputfilenameinstagram.format(phishingoutputfilenameinstagram), 'wb')
if args.a == True or args.gp == True or args.format == "socialmapper":
        titlestring = titlestring + "Google Plus,"
        if args.email is not None:
            phishingoutputfilenamegoogleplus=phishingoutputfilename+"-googleplus.csv"
            filewritergoogleplus = open(phishingoutputfilenamegoogleplus.format(phishingoutputfilenamegoogleplus), 'wb')
if args.a == True or args.vk == True or args.format == "socialmapper":
        titlestring = titlestring + "VKontakte,"
        if args.email is not None:
            phishingoutputfilenamevkontakte=phishingoutputfilename+"-vkontakte.csv"
            filewritervkontakte = open(phishingoutputfilenamevkontakte.format(phishingoutputfilenamevkontakte), 'wb')
if args.a == True or args.wb == True or args.format == "socialmapper":
        titlestring = titlestring + "Weibo,"
        if args.email is not None:
            phishingoutputfilenameweibo=phishingoutputfilename+"-weibo.csv"
            filewriterweibo = open(phishingoutputfilenameweibo.format(phishingoutputfilenameweibo), 'wb')
if args.a == True or args.db == True or args.format == "socialmapper":
        titlestring = titlestring + "Douban,"
        if args.email is not None:
            phishingoutputfilenamedouban=phishingoutputfilename+"-douban.csv"
            filewriterdouban = open(phishingoutputfilenamedouban.format(phishingoutputfilenamedouban), 'wb')
titlestring = titlestring[:-1]
#filewriter.write("Full Name,LinkedIn,Facebook,Twitter,Instagram,Google Plus,Vkontakte,Weibo,Douban\n")
filewriter.write(titlestring)
filewriter.write("\n")
print ""
for person in peoplelist:  
    writestring = '"%s",' % (person.full_name)

    if args.email is not None:
        try:
            # Try to create email by replacing initials and names with persons name
            email = args.email.replace("<first>",person.first_name).replace("<last>",person.last_name).replace("<f>",person.first_name[0]).replace("<l>",person.last_name[0])
        except:
            email = "Error" 

    if args.a == True or args.li == True or args.format == "socialmapper":
        writestring = writestring + '"%s",' % (person.linkedin)
        if person.linkedin != "" and args.email is not None:
            if email != "Error":
                linkedinwritestring = '"%s","%s","%s","%s","%s","%s"\n' % (person.first_name,person.last_name,person.full_name,email,person.linkedin,person.linkedinimage)
                filewriterlinkedin.write(linkedinwritestring)
    if args.a == True or args.fb == True or args.format == "socialmapper":
        writestring = writestring + '"%s",' % (person.facebook)
        if person.facebook != "" and args.email is not None:
            if email != "Error":
                facebookwritestring = '"%s","%s","%s","%s","%s","%s"\n' % (person.first_name,person.last_name,person.full_name,email,person.facebook,person.facebookcdnimage)
                filewriterfacebook.write(facebookwritestring)
    if args.a == True or args.tw == True or args.format == "socialmapper":
        writestring = writestring + '"%s",' % (person.twitter)
        if person.twitter != "" and args.email is not None:
            if email != "Error":
                twitterwritestring = '"%s","%s","%s","%s","%s","%s"\n' % (person.first_name,person.last_name,person.full_name,email,person.twitter,person.twitterimage)
                filewritertwitter.write(twitterwritestring)
    if args.a == True or args.ig == True or args.format == "socialmapper":
        writestring = writestring + '"%s",' % (person.instagram)
        if person.instagram != "" and args.email is not None:
            if email != "Error":
                instagramwritestring = '"%s","%s","%s","%s","%s","%s"\n' % (person.first_name,person.last_name,person.full_name,email,person.instagram,person.instagramimage)
                filewriterinstagram.write(instagramwritestring)
    if args.a == True or args.gp == True or args.format == "socialmapper":
        writestring = writestring + '"%s",' % (person.googleplus)
        if person.googleplus != "" and args.email is not None:
            if email != "Error":
                googlepluswritestring = '"%s","%s","%s","%s","%s","%s"\n' % (person.first_name,person.last_name,person.full_name,email,person.googleplus,person.googleplusimage)
                filewritergoogleplus.write(googlepluswritestring)
    if args.a == True or args.vk == True or args.format == "socialmapper":
        writestring = writestring + '"%s",' % (person.vk)
        if person.vk != "" and args.email is not None:
            if email != "Error":
                vkwritestring = '"%s","%s","%s","%s","%s","%s"\n' % (person.first_name,person.last_name,person.full_name,email,person.vk,person.vkimage)
                filewritervkontakte.write(vkwritestring)
    if args.a == True or args.wb == True or args.format == "socialmapper":
        writestring = writestring + '"%s",' % (person.weibo)
        if person.weibo != "" and args.email is not None:
            if email != "Error":
                weibowritestring = '"%s","%s","%s","%s","%s","%s"\n' % (person.first_name,person.last_name,person.full_name,email,person.weibo,person.weiboimage)
                filewriterweibo.write(weibowritestring)
    if args.a == True or args.db == True or args.format == "socialmapper":
        writestring = writestring + '"%s",' % (person.douban)
        if person.douban != "" and args.email is not None:
            if email != "Error":
                doubanwritestring = '"%s","%s","%s","%s","%s","%s"\n' % (person.first_name,person.last_name,person.full_name,email,person.douban,person.doubanimage)
                filewriterdouban.write(doubanwritestring)

    writestring = writestring[:-1]
    filewriter.write(writestring)
    #filewriter.write('"%s","%s","%s","%s","%s","%s","%s","%s","%s"' % (person.full_name, person.linkedin, person.facebook, person.twitter, person.instagram, person.googleplus, person.vk, person.weibo, person.douban))
    filewriter.write("\n")

    terminalstring = ""
    #print "\n" + person.full_name
    if person.linkedin != "":
        terminalstring = terminalstring + "\tLinkedIn: " + person.linkedin + "\n"
    if person.facebook != "":
        terminalstring = terminalstring +  "\tFacebook: " + person.facebook + "\n"
    if person.twitter != "":
        terminalstring = terminalstring +  "\tTwitter: " + person.twitter + "\n"
    if person.instagram != "":
        terminalstring = terminalstring +  "\tInstagram: " + person.instagram + "\n"
    if person.googleplus != "":
        terminalstring = terminalstring +  "\tGooglePlus: " + person.googleplus + "\n"
    if person.vk != "":
        terminalstring = terminalstring +  "\tVkontakte: " + person.vk + "\n"
    if person.weibo != "":
        terminalstring = terminalstring +  "\tWeibo: " + person.weibo + "\n"
    if person.douban != "":
        terminalstring = terminalstring +  "\tDouban: " + person.douban + "\n"
    if terminalstring != "":
        print person.full_name + "\n" + terminalstring

print "\nResults file: " + outputfilename
filewriter.close()

# Close all the filewriters that may exist

try:
    if filewriterlinkedin:
        filewriterlinkedin.close()
except:
    pass
try:
    if filewriterfacebook:
        filewriterfacebook.close()
except:
    pass

try:
    if filewritertwitter:
        filewritertwitter.close()
except:
    pass
try:
    if filewriterinstagram:
        filewriterinstagram.close()
except:
    pass
try:
    if filewritergoogleplus:
        filewritergoogleplus.close()
except:
    pass
try:
    if filewritervkontakte:
        filewritervkontakte.close()
except:
    pass
try:
    if filewriterweibo: 
        filewriterweibo.close()
except:
    pass
try:
    if filewriterdouban:
        filewriterdouban.close()
except:
    pass


# Code for generating html file
htmloutputfilename = "SM-Results/" + args.input.replace("\"","").replace("/","-") + "-social-mapper.html"
if args.format == "imagefolder":
    htmloutputfilename = "SM-Results/results-social-mapper.html"
filewriter = open(htmloutputfilename.format(htmloutputfilename), 'wb')
#background-color: #4CAF50;
css = """<meta charset="utf-8" />
<style>
    #employees {
        font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
        border-collapse: collapse;
        width: 100%;
    }

    #employees td, #employees th {
        border: 1px solid #ddd;
        padding: 8px;
    }

    #employees td {
        height: 100px;
    }

    #employees tbody:nth-child(even){
        background-color: #f2f2f2;
    }
    
    #employees th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        background-color: #12db00;
        color: white;
    }


    #employees .hasTooltipleft span {
        visibility: hidden;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;

        /* Position the tooltip */
        position: absolute;
        left:15%;
        z-index: 1;

    }

    #employees .hasTooltipcenterleft span {
        visibility: hidden;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;

        /* Position the tooltip */
        position: absolute;
        left:20%;
        z-index: 1;

    }

    #employees .hasTooltipcenterright span {
        visibility: hidden;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;

        /* Position the tooltip */
        position: absolute;
        left:25%;
        z-index: 1;

    }

    #employees .hasTooltipright span {
        visibility: hidden;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;

        /* Position the tooltip */
        position: absolute;
        left:30%;
        z-index: 1;

    }

    #employees .hasTooltipfarright span {
        visibility: hidden;
        background-color: black;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px 0;

        /* Position the tooltip */
        position: absolute;
        left:35%;
        z-index: 1;

    }

    #employees .hasTooltipleft:hover span {
        visibility: visible;
    }

    #employees .hasTooltipcenterleft:hover span {
        visibility: visible;
    }

    #employees .hasTooltipcenterright:hover span {
        visibility: visible;
    }

    #employees .hasTooltipright:hover span {
        visibility: visible;
    }

    #employees .hasTooltipfarright:hover span {
        visibility: visible;
    }

    #employees tbody:hover {
        background-color: #aaa;
    }
}

</style>
"""
foot = "</table></center>"
header = """<center><table id=\"employees\">
            <tr>
                <th rowspan=\"2\">Photo</th>
                <th rowspan=\"2\">Name</th>
                <th>LinkedIn</th>
                <th>Facebook</th>
                <th>Twitter</th>
                <th>Instagram</th>
            </tr>
            <tr>
                <th>GooglePlus</th>
                <th>VKontakte</th>
                <th>Weibo</th>
                <th>Douban</th>
            </tr>
             """
filewriter.write(css)
filewriter.write(header)
for person in peoplelist:  
    body = "<tbody>" \
             "<tr>" \
                "<td class=\"hasTooltipleft\" rowspan=\"2\"><img src=\"%s\" width=auto height=auto style=\"max-width:200px; max-height:200px;\"><span>%s</span></td>" \
                "<td rowspan=\"2\">%s</td>" \
                "<td class=\"hasTooltipcenterleft\"><a href=\"%s\"><img src=\"%s\" onerror=\"this.style.display=\'none\'\" width=auto height=auto style=\"max-width:100px; max-height:100px;\"><span>LinkedIn:<br>%s</span></a></td>" \
                "<td class=\"hasTooltipcenterright\"><a href=\"%s\"><img src=\"%s\" onerror=\"this.style.display=\'none\'\" width=auto height=auto style=\"max-width:100px; max-height:100px;\"><span>Facebook:<br>%s</span></a></td>" \
                "<td class=\"hasTooltipright\"><a href=\"%s\"><img src=\"%s\" onerror=\"this.style.display=\'none\'\" width=auto height=auto style=\"max-width:100px; max-height:100px;\"><span>Twitter:<br>%s</span></a></td>" \
                "<td class=\"hasTooltipfarright\"><a href=\"%s\"><img src=\"%s\" onerror=\"this.style.display=\'none\'\" width=auto height=auto style=\"max-width:100px; max-height:100px;\"><span>Instagram:<br>%s</span></a></td>" \
            "</tr>" \
            "<tr>" \
                "<td class=\"hasTooltipcenterleft\"><a href=\"%s\"><img src=\"%s\" onerror=\"this.style.display=\'none\'\" width=auto height=auto style=\"max-width:100px; max-height:100px;\"><span>GooglePlus:<br>%s</span></a></td>" \
                "<td class=\"hasTooltipcenterright\"><a href=\"%s\"><img src=\"%s\" onerror=\"this.style.display=\'none\'\" width=auto height=auto style=\"max-width:100px; max-height:100px;\"><span>VKontakte:<br>%s</span></a></td>" \
                "<td class=\"hasTooltipright\"><a href=\"%s\"><img src=\"%s\" onerror=\"this.style.display=\'none\'\" width=auto height=auto style=\"max-width:100px; max-height:100px;\"><span>Weibo:<br>%s</span></a></td>" \
                "<td class=\"hasTooltipfarright\"><a href=\"%s\"><img src=\"%s\" onerror=\"this.style.display=\'none\'\" width=auto height=auto style=\"max-width:100px; max-height:100px;\"><span>Douban:<br>%s</span></a></td>" \
            "</tr>" \
            "</tbody>" % (person.person_imagelink, person.person_imagelink, person.full_name, person.linkedin, person.linkedinimage, person.linkedin, person.facebook, person.facebookcdnimage, person.facebook, person.twitter, person.twitterimage, person.twitter, person.instagram, person.instagramimage, person.instagram, person.googleplus, person.googleplusimage, person.googleplus, person.vk, person.vkimage, person.vk, person.weibo, person.weiboimage, person.weibo, person.douban, person.doubanimage, person.douban )
    filewriter.write(body)

filewriter.write(foot)
print "HTML file: " + htmloutputfilename + "\n"
filewriter.close()

# copy images from social mapper to output folder
outputfoldername = "SM-Results/" + args.input.replace("\"","").replace("/","-") + "-social-mapper"
if args.format != "imagefolder":
    os.rename('temp-targets',outputfoldername)
    print "Image folder: " + outputfoldername + "\n"
#if not os.path.exists('temp-targets'):
#    shutil.rmtree('temp-targets')


#print datetime.now() - startTime
#completiontime = datetime.now() - startTime
print "Task Duration: " + str(datetime.now() - startTime)
