import contextlib
import logging
import os
import sys
import datetime
from collections import OrderedDict
import re

import datetime as datetime
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import  FirefoxBinary
import selenium.webdriver.support.ui as ui
from docopt import docopt
import lxml.html
import time
from xvfbwrapper import Xvfb
import subprocess


NOW = datetime.datetime.now()
DATE_TIME_STRING=NOW.strftime("%Y%m%d%H%M%S")

def get_tweet():
    tweet_text=''
    twitter_driver = webdriver.PhantomJS('phantomjs')
    try:

        twitter_driver.get('https://mobile.twitter.com/G6iSkLw88Ugma5N')
        twitter_driver.save_screenshot((get_tweet.__name__ + DATE_TIME_STRING + '_twitter_test_load.png'))
        #Desktop agent # timeline_div = driver.find_element_by_xpath("//div[@id='timeline']/")
        #mobile agent #tweet_text = twitter_driver.find_element_by_xpath("//div[@class='Tweet-body']/*/div[@class='Tweet-text TweetText u-textBreak u-dir']").text
        #mobile no-js agent
        tweet_text = twitter_driver.find_element_by_xpath("//div[@class='tweet-text']/div[@class='dir-ltr']").text

        print 'Tweet string is: '+tweet_text

    except Exception, e:
        # driver.save_screenshot(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')+'.png')
        twitter_driver.save_screenshot((get_tweet.__name__ + DATE_TIME_STRING + '_twitter_test_error.png'))
    return tweet_text


def get_code(tweet_text):
    code = re.search("\d+", tweet_text)
    if code:
        print "code.group() is:"+code.group()
        return code.group()
    print("Unable to extract code from tweet")
    print("What I got was:"+tweet_text)
    exit()


def main():
    # print("Sleeping for 10 mins before checking twitter")
    # time.sleep(600)
    tweet_text=get_tweet()
    return get_code(tweet_text)



if __name__ == '__main__':
    sys.exit(main())