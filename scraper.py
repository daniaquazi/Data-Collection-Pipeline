from nturl2path import url2pathname
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import random
from uuid import uuid4
import json


class Scraper():

    product_list = []
    product_code_list = []

    def __init__(self, _username, _password):
        
        '''
        This function is used to create a constructor to assign values.

        Args:
            username: for typing in a username
            password: for typing in a password
        '''

        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome("/Users/dq/Downloads/chromedriver3")
        # self.driver = webdriver.Chrome("/Users/dq/.wdm/drivers/chromedriver/mac64/101.0.4951.41/chromedriver")
        self.loginurl = "https://instagram.com/"
        self.driver.get(self.loginurl)

        self.posturl = "https://www.instagram.com/p/"

        self.u = _username
        self.p = _password
        self.comments = []

    def get_urls(self):
        
        '''
        This function is used to retrieve URLs of recent instagram posts.
        '''

        username = "chantecaille"
        self.driver.get("https://www.instagram.com/" + username + "/")
        time.sleep(5)
        t_end = time.time() + 60 / 120
        instagram_urls = []
        i = 2
        while i > 0:
            for j in range(1, 2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                posts = self.driver.find_elements_by_xpath('//article[@class = "_aayp"]//div[@class = "_ac7v _aang"]//div[@class = "_aabd _aa8k _aanf"]/a')
                
                #print(len(posts))
                # posts = driver.find_elements_by_tag_name("article")
                # print(len(posts))
                # p = posts.find_elements_by_tag_name("a")
                # print(len(p))
                # print(len(posts))
                for item in posts:
                    url=item.get_attribute("href")
                    instagram_urls.append(url)

            if(time.time() > t_end):
                break

        print("No. of URLs in list", len(instagram_urls))
        a_set = set(instagram_urls)
        instagram_urls = list(a_set)
        print("Unique URLs: ", len(instagram_urls))
        time.sleep(5)
        return instagram_urls

    def accept_cookies(self):

        '''
        This function is used to automatically accept cookies in the instagram webpage.
        '''

        #self.driver.implicitly_wait(10)
        accept_cookies = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Only Allow Essential Cookies')]"))).click()
        time.sleep(5)

    class Product:
        def __init__(self, uuid):
            
            '''
            This function is used to create a constructor to ...

            Args:
                uuid: 
            '''

            self.uuid = uuid
            self.comments = []

        def UUID(self):

            '''
            This function is used to return the UUID.
            '''

            return self.uuid

        def add(self, s):

            '''
            This function is used to append the...

            Args:
                s: 
            '''

            self.comments.append(s)


    def scrape_comments(self):

        '''
        This function is used to scrape the comments from each of the posts.
        '''

    #     insta_url = self.get_urls()
    # #def scrape_comments(self, subject):
    #     # l = ["https://www.instagram.com/p/CeYjnoZOPY9/"]
    #     #url = self.posturl + subject + "/"
    #     try:
    #         self.comments = []
    #         for i in insta_url:
    #             self.driver.get(i)
    #             try:
    #                 num = 100
    #                 for x in range(num):
    #                     time.sleep(5)
    #                     close = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Load more comments"]').click()
    #             except NoSuchElementException:
    #                 pass
    #             p = self.driver.find_elements_by_xpath('.//span[@class = "_aacl _aaco _aacu _aacx _aad7 _aade"]')
    #             for elem in p:
    #                 print(elem.text)
    #                 self.comments.append(elem.text)
    #     except Exception:
    #         print("program ended due to exception")

    #     for x in range(len(self.comments)):
    #         print(self.comments[x])
        o = "https://www.instagram.com/p/CeLuK59A177/"
        insta_urls = []
        insta_urls.append(o)

        #insta_urls = self.get_urls()
        try:
            #comments = []
            self.product_list.clear()
            self.product_code_list.clear()
            # print("at start: ")
            # print("product list is: ")
            # for y in self.product_list:
            #     print(y + "   ", end =" ")
            # print(" ")
            # print("finsihed init")

            # print("product code list is: ")
            # for y in self.product_code_list:
            #     print(y + "   ", end =" ")
            # print(" ")

            for c in insta_urls:
                self.driver.get(c)
                try:
                    num = 100
                    for x in range(num):
                        time.sleep(5)
                        close = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Load more comments"]').click()
                except NoSuchElementException:
                    pass
                self.product_code_list = [i.rsplit('/', 2)[-2] for i in insta_urls]
                # print("product list after creation: ")
                # for y in self.product_list:
                #     print(y + "   ", end =" ")
                # print(" ")
                # print("after creation")
                t = Scraper.Product(str(uuid4()))
                # print("10")
                self.product_list.append(t)
                p = self.driver.find_elements_by_xpath('.//span[@class = "_aacl _aaco _aacu _aacx _aad7 _aade"]')
                # print("12")
                for elem in p:
                    #print(elem.text)
                    t.add(elem.text)

        except Exception:
            print("program ended due to exception")

        self.dictionary = dict(zip(self.product_code_list, self.product_list))
        # for key in dictionary.keys():
        #     p = dictionary[key]
        #     print(key, "   ", p.UUID())
        #     for i in p.comments:
        #         print(i)

    def dump_product(self, fp, key):

        '''
        This function is used to ...

        Args:
            fp:
            key: 
        '''

        if(key in self.dictionary.keys()):
            p = self.dictionary[key]
            json.dump(key + "," + p.UUID(), fp)
            for i in p.comments:
                json.dump(","+i, fp)
        else:
            print("Error in dictionary. Key " + str(key) + " was not found")

        print(p.comments)
        


    def dump_products(self, file_name):

        '''
        This function is used to loop over all the keys and dump all the info into a file.

        Args:
            file_name: the name of the file
        '''

        with open(file_name, "w") as fp:
            for key in self.dictionary.keys():
                self.dump_product(fp, key)

    def save_information(self):
        self.save_info = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))).click()
        time.sleep(5)
        self.turn_on_notifs = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
        time.sleep(5)
        print("done") #input("Press enter to exit")

    def login(self):
        # self.accept_cookies()
        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        username.clear()
        password.clear()
        #username.send_keys("dummypracticetest2")
        #password.send_keys("dummy12345")
        username.send_keys(self.u)
        password.send_keys(self.p)
        log_in = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        time.sleep(5)
        # turn off notifications
        # self.save_information()
        # time.sleep(5)
        # self.scrape_comments()

        # print("keys are ")
        # print(self.dictionary.keys())
        # print("product list is: ")
        # for y in self.product_code_list:
        #     print(y + "   ", end =" ")
        # print(" ")
        # file_name = "/Users/dq/Documents/savesss_output.txt"
        # with open(file_name, "w") as fp:
        #     json.dump("teststring", fp)
        #     for key in self.product_code_list:
        #         print("searching for: " + key)
        #         # self.dump_product(fp, key)
        #         if(key in self.dictionary):
        #             p = self.dictionary[key]
        #             json.dump(str(key) + "   " + p.UUID(), fp)
        #             for i in p.comments:
        #                 json.dump(i, fp)
        #         else:
        #             print("Error in dictionary. Key " + str(key) + " was not found")

    def initialize_comments(self):
        self.comments = []
    
    def post_comments(self):
        compliment = random.choice(['niceee', 'fabulous!', 'great', 'love it!', 'follow me guys', u'\u2764'])
        self.comment = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "Ypffh")))
        self.comment.click()
        self.comment.send_keys(compliment)
        self.comment.send_keys(Keys.ENTER)

    def get_urls2(self):
        
        '''
        This function is used to retrieve URLs of recent instagram posts.
        '''

        username = "chantecaille"
        self.driver.get("https://www.instagram.com/" + username + "/")
        time.sleep(5)
        t_end = time.time() + 60 / 120
        instagram_urls = []
        i = 2
        while i > 0:
            for j in range(1, 2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                posts = self.driver.find_elements_by_xpath('//article[@class = "_aayp"]//div[@class = "_ac7v _aang"]//div[@class = "_aabd _aa8k _aanf"]/a')
                
                #print(len(posts))
                # posts = driver.find_elements_by_tag_name("article")
                # print(len(posts))
                # p = posts.find_elements_by_tag_name("a")
                # print(len(p))
                # print(len(posts))
                for item in posts:
                    url=item.get_attribute("href")
                    instagram_urls.append(url)

            if(time.time() > t_end):
                break

        print("No. of URLs in list", len(instagram_urls))
        a_set = set(instagram_urls)
        instagram_urls = list(a_set)
        print("Unique URLs: ", len(instagram_urls))
        time.sleep(5)
        return instagram_urls

    def scrape_comments2(self):

        '''
        This function is used to scrape the comments from each of the posts.
        '''

        insta_url = ["https://www.instagram.com/p/Ce3q7pfgOeL/"]
    #def scrape_comments(self, subject):
        # l = ["https://www.instagram.com/p/CeYjnoZOPY9/"]
        #url = self.posturl + subject + "/"
        try:
            self.comments = []
            for i in insta_url:
                self.driver.get(i)
                try:
                    num = 100
                    for x in range(num):
                        time.sleep(5)
                        close = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Load more comments"]').click()
                except NoSuchElementException:
                    pass
                p = self.driver.find_elements_by_xpath('.//span[@class = "_aacl _aaco _aacu _aacx _aad7 _aade"]')
                for elem in p:
                    print(elem.text)
                    self.comments.append(elem.text)
        except Exception:
            print("program ended due to exception")

        # for x in range(len(self.comments)):
        #     print(self.comments[x])
        # o = "https://www.instagram.com/p/CeLuK59A177/"
        # insta_urls = []
        # insta_urls.append(o)

        # insta_urls = self.get_urls()
        # try:
        #     #comments = []
        #     self.product_list.clear()
        #     self.product_code_list.clear()
        #     # print("at start: ")
        #     # print("product list is: ")
        #     # for y in self.product_list:
        #     #     print(y + "   ", end =" ")
        #     # print(" ")
        #     # print("finsihed init")

        #     # print("product code list is: ")
        #     # for y in self.product_code_list:
        #     #     print(y + "   ", end =" ")
        #     # print(" ")

        #     for c in insta_urls:
        #         self.driver.get(c)
        #         try:
        #             num = 100
        #             for x in range(num):
        #                 time.sleep(5)
        #                 close = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Load more comments"]').click()
        #         except NoSuchElementException:
        #             pass
        #         self.product_code_list = [i.rsplit('/', 2)[-2] for i in insta_urls]
        #         # print("product list after creation: ")
        #         # for y in self.product_list:
        #         #     print(y + "   ", end =" ")
        #         # print(" ")
        #         # print("after creation")
        #         t = Scraper.Product(str(uuid4()))
        #         # print("10")
        #         self.product_list.append(t)
        #         p = self.driver.find_elements_by_xpath('.//span[@class = "_aacl _aaco _aacu _aacx _aad7 _aade"]')
        #         # print("12")
        #         for elem in p:
        #             #print(elem.text)
        #             t.add(elem.text)

        # except Exception:
        #     print("program ended due to exception")

        # self.dictionary = dict(zip(self.product_code_list, self.product_list))
        # # for key in dictionary.keys():
        # #     p = dictionary[key]
        # #     print(key, "   ", p.UUID())
        # #     for i in p.comments:
        # #         print(i)