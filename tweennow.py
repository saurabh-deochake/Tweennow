#!/usr/bin/env python

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from sys import version_info
from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser
from params import *
import os
import json
import re
import time
import __future__
import logging
import tweepy




"""
Author: Saurabh Deochake (saurabh.d04@gmail.com)

Note: Before you run this script, please get your Consumer Key, Consumer Secret,
Access Token and Access Secret Keys from https://dev.twitter.com by creating your
own app

"""
    


class Tweennow:
    def get_api(self):
        return tweepy.API(auth)
    
    def call_api(self):
    
        api = self.get_api()
    
        woeidDict = {}
        
        areas = api.trends_available()
        
        for area in areas:
            name = area["name"]
            woeid = area["woeid"]
            woeidDict[name]= woeid
        
        
        parser = SafeConfigParser()
        parser.read(CONFIG_FILE)
        location = parser.get('geo','location')
        
        if woeidDict.has_key(location):
            woeidLocation = woeidDict[location]
        else:
            logger.warning("Location WOEID not found!")
        
        
        trends1 = api.trends_place(woeidLocation) # from the end of your code
        # trends1 is a list with only one element in it, which is a 
        # dict which we'll put in data.
        data = trends1[0] 
        # grab the trends
        trends = data['trends']
        # grab the name from each trend
        names = [trend['name'] for trend in trends]
        # put all the names together with a ' ' separating them
        
        
        
        #print woeidDict[]
        
        print "\n\n\n***** WELCOME TO TWEENNOW *****"
        print "\n Fetching trending topics...\n"
        time.sleep(2)
        
        trendsDict = {}
        numbers = 1
        for trend in names:
            print str(numbers)+") "+trend
            trendsDict[numbers] = trend
            numbers = numbers +1
        
        #print trendsDict
        selection = raw_input("\n\nEnter the number corrosponding to trends (Enter 0 to input your own topic):")    
            
        if int(selection) in range(1,11):
            query = trendsDict[int(selection)]
        elif int(selection) == 0:
            query = raw_input("You have selected option 0. Please enter your topic: ")
            
        print "\nShowing the tweets about",query,"on your desktop.\n\n"   
        
        twitterStream = Stream(auth, Messenger())
        twitterStream.filter(track=[query])  #Track tweets with any hashtags/Word
    
        
        
    def authenticate(self):
        
        parser = SafeConfigParser()
        if not os.path.exists(CONFIG_FILE):
            logger.error("Configuration file does not exist.")
        elif not os.path.isfile(CONFIG_FILE):
            logger.error("Configuration file is not a valid file.")
        else:
            parser.read(CONFIG_FILE)
            
        logger.info("Fetching authentication data")
        ckey = parser.get('token','ckey')
        csecret = parser.get('token','csecret')
        atoken = parser.get('token','atoken')
        asecret = parser.get('token','asecret')
        
        return ckey,csecret,atoken, asecret
    

class Messenger(StreamListener):
    
    #using pynotify module to send messages on desktop        
    def popUpMessage(self,message):
        if notifyModule is "pynotify":
            logger.debug("Initializing pynotify")
            pynotify.init("Tweennow")
            logger.debug("Sending notification: message:{}".format(message))
            pynotify.Notification(message).show()
        elif notifyModule is "Notify":
            logger.debug("Initializing Notify")
            Notify.init("Tweennow")
            logger.debug("Sending notification: message:{}".format(message))
            Notify.Notification.new(message).show()
        else:
            logger.debug("Initializing notify2")
            notify2.init("Tweennow")
            logger.debug("Sending notification: message:{}".format(message))
            notify2.Notification(message).show()
        

    def on_data(self, data):
        try:
            
            #Take out username 
            userName = data.split(',"screen_name":"')[1].split('","location')[0]
            #Take out actual tweet
            tweet = data.split(',"text":"')[1].split('","source')[0]
            logger.debug("Fetching Tweets")
            #Create message in format: @username: <text>
            fetchedTweet = "@"+userName+"-"+tweet
            
            #Call popUpMessage() to send your message to desktop
            logger.debug("Sending Tweets")
            self.popUpMessage(fetchedTweet)
            time.sleep(7)
            return True
        
        except BaseException, e:
            print 'Failed Ondata,', str(e)
            logger.error(str(e))
            time.sleep(5)
        except KeyboardInterrupt, k:
            print 'Keyboard Interrupt Occured,',str(k)
            logger.error(str(k))
            quit()

    def on_error(self, status):
        print status

if __name__ == '__main__':
    
    
    
    if version_info.major is 2:
        import pynotify
        notifyModule = "pynotify"
    if version_info.major is 3:
        try:
            from gi.Repository import Notify
            notifyModule = "Notify"
        except ImportError:
            import notify2
            notifyModule = "notify2"

    # Setting the logger
    
    logger = logging.getLogger('tweennow')
    parser = SafeConfigParser()
    parser.read(CONFIG_FILE)
    logFile = parser.get('logging','log_file')
    
    hdlr = logging.FileHandler(logFile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr) 
    logger.setLevel(logging.DEBUG)

    #Creating an object of Tweennow
    logger.info("Creating an instance of Tweennow")
    tObj = Tweennow()
    
    logger.info("Authenticating the user's credentials")
    ckey, csecret, atoken, asecret = tObj.authenticate()
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    
    logger.info("User successfully authenticated.")
    
    tObj.call_api()
    
    