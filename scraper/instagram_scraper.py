from nturl2path import url2pathname
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import time
import random
from uuid import uuid4
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import pandas as pd
import boto3
from sqlalchemy import create_engine
import psycopg2
import boto3
import json
import ast
import re
import psycopg2
import bs4
from time import sleep
import os
import io

class Scraper():
    def __init__(self, _username, _password):

        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"')

        self.driver = webdriver.Firefox(options = options)
        self.loginurl = "https://instagram.com/"
        self.driver.get(self.loginurl)
        # self.driver.implicitly_wait(40)
        
       
        self.posturl = "https://www.instagram.com/p/"

        self.u = _username
        self.p = _password
        self.comments = []

    def get_urls(self):
        username = "fredericmalle"
        time.sleep(5)
        self.driver.get("https://www.instagram.com/" + username + "/")
        # self.driver.get_screenshot_as_png("/scraper_folder/scraper.png")
        time.sleep(5)
        t_end = time.time() + 60 / 120
        instagram_urls = []
        i = 2
        while i > 0:
            for j in range(1, 2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # self.export_page_source("after_login")
                # self.driver.get_screenshot_as_file("/scraper_folder/after_login.png")

                posts = self.driver.find_elements(by=By.XPATH, value='//article[@class = "_aayp"]//div[@class = "_ac7v _aang"]//div[@class = "_aabd _aa8k _aanf"]/a')
                
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

    def create_uuids_for_url_list(self):
        url = self.get_urls()
        ig_urls = [i.rsplit('/', 2)[-2] for i in url]
        uuid_list = [str(uuid4()) for x in ig_urls]
        dic = [str(x[0]) + '--' + x[1] for x in zip(ig_urls, uuid_list)]
        url_list = {'Unique Code':dic, 'URL':url}
        df = pd.DataFrame(url_list)

        for column in df:
            s = df['URL'].values
        s = list(s)
        return s

    def accept_cookies(self):
        #self.export_page_source("htmltext2")
        #html_file = self.export_page_source("cookies")


        # html = self.driver.page_source
        # s3.upload_fileobj(html, 'daniascraper', 'htmll.txt')
        
        time.sleep(10)
        #self.driver.find_element_by_xpath(By=By.XPATH, value="//body").send_keys(Keys.END)
        try:
            try:
                # print(self.driver.page_source)
                accept_cookies = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Only allow essential cookies')]"))).click()
                print("cookies button found")
            except (TimeoutException, NoSuchElementException):
                #print("Cookies button not found")
                try:
                    accept_cookies = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Only Allow Essential Cookies')]"))).click()
                    print("cookies button found")
                except (TimeoutException, NoSuchElementException):
                    print("Cookies button not found")
        except Exception:
            pass
                
        #self.driver.implicitly_wait(10)
        time.sleep(5)

    def scrape_comments(self):
        count = 0
        insta_urls = self.create_uuids_for_url_list()
        #insta_urls = ['https://www.instagram.com/p/CfW7ad2h29I/', 'https://www.instagram.com/p/CfZIJfmDKsO/']
        try:
            comments = []
            for i in insta_urls:
                time.sleep(5)
                self.driver.get(i)

                # screenshot = self.driver.get_screenshot_as_png()
                # s3 = boto3.client('s3', aws_access_key_id='', aws_secret_access_key='', region_name='us-east-1')
                # png = io.BytesIO(screenshot)
                # s3.upload_fileobj(png, 'daniascraper', 'post.png')

                count = count + 1
                print(count)
                try:
                    num = 100
                    for x in range(num):
                        time.sleep(5)
                        close = self.driver.find_element(By.CSS_SELECTOR, '[aria-label="Load more comments"]').click()
                except NoSuchElementException:
                    pass
                p = self.driver.find_elements(by=By.XPATH, value='.//span[@class = "_aacl _aaco _aacu _aacx _aad7 _aade"]')
                for elem in p:
                    # print(elem.text)
                    comments.append({"URL":i, "comments":elem.text})

        except Exception:
            print("program ended due to exception")
        print("no of values: ", len(comments))
        df = pd.DataFrame(comments)
        
        return df

    def perform_sentiment_analysis(self):
        comments = self.scrape_comments()
        sAnalyser = SentimentIntensityAnalyzer()
        comments['comments'] = comments['comments'].astype(str)
        comments['scores'] = comments['comments'].apply(sAnalyser.polarity_scores)
        comments['compound_score'] = [sAnalyser.polarity_scores(x)['compound'] for x in comments['comments']]
        comments_scores = []
        for row in comments['compound_score']:
            if row >= 0.05: comments_scores.append('positive')
            elif row <= -0.05: comments_scores.append('negative')
            else: comments_scores.append('neutral')
        comments['comments_result'] = comments_scores
        comments['sentiment_analysis_score'] = comments['compound_score'].round(1)
        comments = comments.drop(['scores'], axis=1)
        comments = comments.drop(['compound_score'], axis=1)
        comments = comments.astype('string')
        return comments

    def retry_click(self, number_of_retries, wait_before_performing_click):
        while number_of_retries > 0:
            time.sleep(wait_before_performing_click)
            try:
                self.turn_on_notifs = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
                break
            except:
                pass
            number_of_retries = number_of_retries - 1
            print(number_of_retries)

    def save_information(self):
        try:
            self.save_info = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Not now')]"))).click()
        except (TimeoutException, NoSuchElementException):
            pass
        # self.save_info = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not now')]")
        # self.save_info.click()
        # element_to_be_clickable
            time.sleep(5)
        try:
            self.turn_on_notifs = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
        except (TimeoutException, NoSuchElementException):
            pass
        # self.turn_on_notifs = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        # self.turn_on_notifs.click()
        # try:
        #     self.turn_on_notifs = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='(text(), 'Not Now')]"))).click()
        #     print('Clicked it')
        # except:
        #     print('Either element was not found, or Bot could not click on it.')
        #     self.driver.refresh()
        #     self.retry_click(20, 10)
        #     pass
        # time.sleep(5)



    def login(self):
        sleep(2)

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
        time.sleep(10)
        # print(self.driver.page_source)
        

    def export_page_source(self, filepath : str):
        soup = self.driver.page_source
        soup = bs4.BeautifulSoup(soup,"html.parser")
        soup = str(soup.prettify)
        
        with open(f"/Users/dq/Documents/instagram_scraper/scraper_folder/{filepath}.txt", 'w') as f:
        # with open(f"{filepath}.txt", 'w') as f:
            f.write(soup)

if __name__ == "__main__":
    username = ['dummypracticetest', 'dummypracticetest2', 'dummypracticetest3']
    user = random.choice(username)
    s = Scraper(user, "dummy12345")
    s.accept_cookies()
    s.login()
    time.sleep(5)
    s.save_information()
    insta_comments = s.perform_sentiment_analysis()
    print(insta_comments)

    from sqlalchemy import create_engine
    DATABASE_TYPE = 'postgresql'
    DBAPI = 'psycopg2'
    ENDPOINT = 'postgres.cgvbzgiyidpp.us-east-1.rds.amazonaws.com'
    USER = 'postgres'
    PASSWORD = 'rdsdatabasepassword'
    PORT = 5432
    DATABASE = 'postgres'
    engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
    c = engine.connect()

    insta_comments.to_sql('test', engine, if_exists='append')

    # s3 = boto3.client('s3')
    # bucket = s3.create_bucket(Bucket='scraper26510', CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})
    # s3 = boto3.resource('s3')
    # s3.meta.client.upload_file('/Users/dq/Documents/savesss_output.txt', 'daniascraper', 'savesss_output.txt')
    # s3.list_objects(Bucket='daniascraper')