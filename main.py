#!/usr/bin/env python
# encoding: utf-8


"""
CMFCU Scraper
Usage:
  cmfcu-scraper [--local]

Options:
  -h --help                      Show this help.
  --local                      Run locally.
  --auth=<username>:<password>   Vodafone username/password. If not supplied,
                                 the environment variables VODAFONE_USERNAME
                                 and VODAFONE_PASSWORD are used.
"""

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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import selenium.webdriver.support.ui as ui
from docopt import docopt
import lxml.html
import time
from xvfbwrapper import Xvfb
import subprocess

LOGIN_URL = 'https://ob.cmcu.org/User/AccessSignin/Start'
FIREFOX_BINARY_PATH = None
FIREFOX_PROFILE_PATH = None
NOW = datetime.datetime.now()
DATE_TIME_STRING = NOW.strftime("%Y%m%d%H%M%S")
driver = webdriver.PhantomJS('phantomjs')
wait=driver.WebDriverWait(driver, 10)


def get_username_password():
    """
    Parse the username/password from the command line or environment.
    """
    # username = os.environ.get('CMFCU_USERNAME')
    # password = os.environ.get('CMFCU_PASSWORD')
    username = 'username'
    password = 'password'
    return username, password


def drive_to_security_code(username, password):
    """

    :rtype: phantomdriver
    """
    wait.until(lambda driver: 'Charlotte Metro Federal Credit Union' in driver.title)
    assert "Charlotte Metro Federal Credit Union" in driver.title
    username_box = driver.find_element_by_name('UsernameField')
    username_box.send_keys(username)
    driver.find_element_by_name('SubmitNext').click()
    wait.until(lambda driver: driver.find_element_by_name('PasswordField'))
    logging.debug("Now entering password.")
    password_box = driver.find_element_by_name('PasswordField')
    password_box.send_keys(password)
    print("Got to step 9")
    final_submit_button = driver.find_element_by_name('SubmitNext')
    final_submit_button.click()
    print("Got to step 10")
    filename=('drive_to_security_code_' + DATE_TIME_STRING + '_load.png')
    driver.save_screenshot(filename)
    write_log(filename)


def custom_firefox_profile(images=False, css=False, flash=False):
    """
    Create a new Firefox profile with some custom configuration.
    """

    profile = FirefoxProfile()
    if not css:
        profile.set_preference('permissions.default.stylesheet', 2)
    if not images:
        profile.set_preference('permissions.default.image', 2)
    if not flash:
        profile.set_preference(
            'dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    return profile


def get_tweet():
    tweet_text = ''
    twitter_driver = webdriver.PhantomJS('phantomjs')
    try:

        twitter_driver.get('https://mobile.twitter.com/G6iSkLw88Ugma5N')
        twitter_driver.save_screenshot((get_tweet.__name__ + DATE_TIME_STRING + '_twitter_test_load.png'))
        # Desktop agent # timeline_div = driver.find_element_by_xpath("//div[@id='timeline']/")
        # mobile agent #tweet_text = twitter_driver.find_element_by_xpath("//div[@class='Tweet-body']/*/div[@class='Tweet-text TweetText u-textBreak u-dir']").text
        # mobile no-js agent
        tweet_text = twitter_driver.find_element_by_xpath("//div[@class='tweet-text']/div[@class='dir-ltr']").text

        print 'Tweet string is: ' + tweet_text

    except Exception, e:
        # driver.save_screenshot(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')+'.png')
        twitter_driver.save_screenshot((get_tweet.__name__ + DATE_TIME_STRING + '_twitter_test_error.png'))
    return tweet_text


def get_code(tweet_text):
    code = re.search("\d+", tweet_text)
    if code:
        print "code.group() is:" + code.group()
        return code.group()
    print("Unable to extract code from tweet")
    print("What I got was:" + tweet_text)
    exit()


def write_log(filename,text):
    text_file = open(filename+'.txt', "w")
    text_file.write(text)
    text_file.close()

def get_code_from_twitter():
    print("Sleeping for 9 mins before checking twitter")
    driver.WebDriverWait(driver, 540)
    tweet_text = get_tweet()
    return get_code(tweet_text)


def drive_past_security():
    # First time logging in need to Send Sign in Security Code
    # try:

    wait.until(lambda driver: driver.find_element_by_name('DeliverField'))
    print ("deliverField Found. Attempting to select email message")
    #driver.find_element_by_xpath("//select[@name='DeliverField']/option[value()='M:26069699E6BE4CB99FF8213D13CDD3B3AB86B0FBAFA59484']").click()  # For Email Message
    driver.find_element_by_xpath(
        "//option[value()='M:26069699E6BE4CB99FF8213D13CDD3B3AB86B0FBAFA59484']").click()  # For Email Message
    print("Code by Text message selected")
    driver.find_element_by_name('SubmitNext').click()
    driver.save_screenshot(('drive_past_security' + DATE_TIME_STRING + '_load.png'))
    driver.page_source()

    security_code = get_code_from_twitter()

    print "Typing in security code"
    security_code_box = driver.find_element_by_name('PasscodeField')
    security_code_box.send_keys(security_code)
    filename= 'drive_past_security' + DATE_TIME_STRING + '_security.png'
    driver.save_screenshot(filename)
    write_log(filename)
    driver.find_element_by_name('SubmitNext').click()
    print"drive_past_security method complete"


def get_accounts_page_html(username, password):
    """
    Use the Selenium webdriver to log into the Vodafone site and return the
    HTML of the front page, after it's finished rendering the summary usage
    in Javascript.
    """

    try:
        # with contextlib.closing(webdriver.Firefox(firefox_profile=custom_firefox_profile(images=False, css=True, flash=False),firefox_binary=FirefoxBinary(firefox_path='/home/gabefair0/bin/firefox/firefox'))) as driver:

        # subprocess.call('ls '+binary_path, shell=True)
        print "We are in the process with PID= %d" % os.getpid()
        # vdisplay = xvfbwrapper.Xvfb()
        # vdisplay.start()
        # driver.add_cookie({'6D6FAB4AC33945DE4FA13219E064BD66': 'key', 'value': 'value', 'path': '/'})
        # print("Add Cookies Complete")
        print("Got to step 1")

        drive_to_security_code(username, password)
        drive_past_security()
        print "Now logged in"
        # Now logged in
        #driver.save_screenshot(('main' + DATE_TIME_STRING + '_now-logged_in.png'))

        wait.until(lambda driver: driver.find_element_by_name('Criteria'))
        print("Got to step 11")
        driver.get('https://ob.cmcu.org/User/CustomTransferToShare/Start')
        print("Got to step 12")
        amount_box = driver.find_element_by_name('AmountField')
        amount_box.send_keys('500')
        print("Got to step 13")
        driver.find_element_by_xpath("//select[@name='AccountNumberIdFromField']/option[value()='card']").click()
        time.sleep(6)
        wait.until(lambda driver: driver.find_element_by_name('CardNumber'))
        print("Got to step 14")
        card_number_box = driver.find_element_by_name('CardNumber')
        card_number_box.send_keys('5555555555555555')

        cvv_number_box = driver.find_element_by_name('CardCVV')
        cvv_number_box.send_keys('555')

        driver.find_element_by_xpath("//select[@name='CreditCardMonth']/option[text()='April']").click()
        driver.find_element_by_xpath("//select[@name='CreditCardYear']/option[text()='2019']").click()
        print("Got to step 15")
        driver.find_element_by_xpath("//select[@name='AccountNumberIdToField']/option[3]").click()
        # print(driver.page_source)
        driver.find_element_by_name('SubmitNext').click()
        print("Got to step 16")
        # print(driver.page_source)
        wait.until(lambda driver: driver.find_element_by_name('SubmitNext'))
        print("Got to step 17")
        driver.find_element_by_name('SubmitNext').click()
        print("Got to end")
        # vdisplay.stop()
        driver.close()
        print("Complete")
    except Exception, e:
        print e
        driver.save_screenshot((get_accounts_page_html.__name__ + DATE_TIME_STRING + '_exception.png'))
    return 0


def main():
    options = docopt(__doc__, version='1.0.1')
    if options['--local']:
        logging.basicConfig(level=logging.DEBUG)
        FIREFOX_BINARY_PATH = "C:\Program Files (x86)\Mozilla Firefox\\firefox.exe"
        print("Got to step 1")
        FIREFOX_PROFILE = custom_firefox_profile(images=False, css=True, flash=False)
        firefox_binary = FirefoxBinary(firefox_path=FIREFOX_BINARY_PATH)
        print("Got to step 2")
        driver = webdriver.Firefox(firefox_profile=FIREFOX_PROFILE)
    else:
        logging.basicConfig(level=logging.INFO)
        FIREFOX_BINARY_PATH = "/home/gabefair0/bin/firefox/firefox"

    username, password = get_username_password()

    if not username or not password:
        print("No username/password supplied. Either pass on the command line "
              "or set VODAFONE_USERNAME and VODAFONE_PASSWORD in your "
              "environment.")
        return 1

    # subprocess.call('ls /home/gabefair0/bin/firefox/',shell=True)
    get_accounts_page_html(username, password)
    return 0


if __name__ == '__main__':
    sys.exit(main())
