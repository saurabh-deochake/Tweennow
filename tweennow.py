#!/usr/bin/env python

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from sys import version_info
from bs4 import BeautifulSoup
from ConfigParser import SafeConfigParser
from params import *
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

def authenticate():
    print CONFIG_FILE
    
    parser = SafeConfigParser()
    parser.read(CONFIG_FILE)
    
    ckey = parser.get('token','ckey')
    csecret = parser.get('token','csecret')
    atoken = parser.get('token','atoken')
    asecret = parser.get('token','asecret')
    
    return ckey,csecret,atoken, asecret

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

#using pynotify module to send messages on desktop        
def popUpMessage(message):
    if notifyModule is "pynotify":
        logging.debug("Initializing pynotify")
        pynotify.init("Tweennow")
        logging.debug("Sending notification: message:{}".format(message))
        pynotify.Notification(message).show()
    elif notifyModule is "Notify":
        logging.debug("Initializing Notify")
        Notify.init("Tweennow")
        logging.debug("Sending notification: message:{}".format(message))
        Notify.Notification.new(message).show()
    else:
        logging.debug("Initializing notify2")
        notify2.init("Tweennow")
        logging.debug("Sending notification: message:{}".format(message))
        notify2.Notification(message).show()
        
class listener(StreamListener):

    def on_data(self, data):
        try:
            
            #Take out username 
            userName = data.split(',"screen_name":"')[1].split('","location')[0]
            #Take out actual tweet
            tweet = data.split(',"text":"')[1].split('","source')[0]
            
            #Create message in format: @username: <text>
            fetchedTweet = "@"+userName+"-"+tweet
            
            #Call popUpMessage() to send your message to desktop
            popUpMessage(fetchedTweet)
            time.sleep(7)
            return True
        
        except BaseException, e:
            print 'Failed Ondata,', str(e)
            time.sleep(5)
        except KeyboardInterrupt:
            if didInterrupt:
                logging.info("keyboard interrupted, once")
                print("Bye bye")
                quit()

    def on_error(self, status):
        print status

ckey, csecret, atoken, asecret = authenticate()
auth = OAuthHandler(ckey, csecret)

print "Auth done"
auth.set_access_token(atoken, asecret)
print "access done"
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#AUSvNZ"])  #Track tweets with any hashtags/Word
