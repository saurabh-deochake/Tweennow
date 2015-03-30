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



"""
Author: Saurabh Deochake (saurabh.d04@gmail.com)

Note: Before you run this script, please get your Consumer Key, Consumer Secret,
Access Token and Access Secret Keys from https://dev.twitter.com by creating your
own app

"""
    


class Tweennow:
    
        
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
    
    twitterStream = Stream(auth, Messenger())
    twitterStream.filter(track=["AAP"])  #Track tweets with any hashtags/Word
