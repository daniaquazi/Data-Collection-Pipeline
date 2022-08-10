from instagram_scraper import Scraper
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
    # def test_login(self):
    #     s = Scraper("dummypracticetest2", "dummy123")
    #     s.accept_cookies()
    #     try:
    #         t = s.login()
    #     except:
    #         self.assertIsNone(t)

    # def test_scrape_comments(self):
    #     p = []
    #     s = Scraper("dummypracticetest", "dummy123456")
    #     s.accept_cookies()
    #     s.login()
    #     s.save_information()
    #     time.sleep(5)
    #     # p = s.get_urls2()
    #     # o = p[0]
    #     test = s.scrape_comments()
    #     self.assertIsNone(test)

    # testing to see if a URL exists (code 200 means the request was successful)
    # def test_get_urls(self):
    #     p = []
    #     s = Scraper("dummypracticetest3", "dummy123456")
    #     s.accept_cookies()
    #     s.login()
    #     s.save_information()
    #     time.sleep(5)
    #     # s.get_urls()
    #     p = s.get_urls()
    #     o = p[0]
    #     ret = urllib.urlopen(o)
    #     self.assertTrue(ret.code == 200)

    # def test_sort_by_date(self):
    #     p = []
    #     s = Scraper("dummypracticetest4", "dummy123456")
    #     s.accept_cookies()
    #     s.login()
    #     s.save_information()
    #     time.sleep(5)
    #     # s.get_urls()
    #     p = s.sort_by_date()
    #     o = p[0]
    #     print(o)
    #     self.assertTrue(o)

    # def test_create_uuids_for_url_list(self):
    #     s = Scraper("dummypracticetest3", "dummy123456")
    #     s.accept_cookies()
    #     s.login()
    #     s.save_information()
    #     time.sleep(5)
    #     s.get_urls()
    #     i = s.create_uuids_for_url_list()
    #     self.assertTrue(i)

    # def test_accept_cookies(self):
    #     s = Scraper("dummypracticetest4", "dummy123456")
    #     i = s.accept_cookies()
    #     self.assertIsNone(i)
    
    # def test_login(self):
    #     p = []
    #     s = Scraper("dummypracticetest4", "dummy123456")
    #     s.accept_cookies()
    #     i = s.login()
    #     self.assertIsNone(i)

    # def test_save_info(self):
    #     p = []
    #     s = Scraper("dummypracticetest4", "dummy123456")
    #     s.accept_cookies()
    #     s.login()
    #     i = s.save_information()
    #     self.assertIsNone(i)

    def test_save_in_s3(self):
        s = Scraper("dummypracticetest4", "dummy123456")
        s.accept_cookies()
        i = s.save_in_s3('test.png')
        self.assertIsNone(i)

unittest.main()



