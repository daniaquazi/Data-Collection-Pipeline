from scraper import Scraper
import unittest
from nturl2path import url2pathname
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import time
import requests
import urllib.request as urllib

class testing(unittest.TestCase):

    # testing wrong log in details to check if it fails
    def test_login(self):
        s = Scraper("dummypracticetest2", "dummy123")
        s.accept_cookies()
        try:
            t = s.login()
        except:
            self.assertIsNone(t)

    # test if a file directory exists
    def test_dump_products(self):
        path = "/Users/dq/Documents/savesss_output.txt"
        isFile = os.path.isfile(path) 
        self.assertTrue(isFile)

    def test_scrape_comments(self):
        p = []
        s = Scraper("dummypracticetest", "dummy123456")
        s.accept_cookies()
        s.login()
        s.save_information()
        time.sleep(5)
        # p = s.get_urls2()
        # o = p[0]
        test = s.scrape_comments()
        self.assertIsNone(test)

    # testing to see if a URL exists (code 200 means the request was successful)
    def test_get_urls(self):
        p = []
        s = Scraper("dummypracticetest3", "dummy123456")
        s.accept_cookies()
        s.login()
        s.save_information()
        time.sleep(5)
        # s.get_urls()
        p = s.get_urls()
        o = p[0]
        ret = urllib.urlopen(o)
        self.assertTrue(ret.code == 200)

unittest.main()



