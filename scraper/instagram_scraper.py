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
import psycopg2
import bs4
from time import sleep
import os
import io
from urllib.request import urlopen
from bs4 import BeautifulSoup
import base64

class Scraper():

    def __init__(self, _username, _password):

        '''
        This function is used to create a constructor to assign values.

        Args:
            username: for typing in a username
            password: for typing in a password
        '''

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
    
    def save_in_s3(self, image_name):

        '''
        This function is used to send images into an S3 bucket

        Args:
            image_name: for entering the name of the image
        '''

        screenshot = self.driver.get_screenshot_as_png()
        s3 = boto3.client('s3', aws_access_key_id = "", aws_secret_access_key = "", region_name='us-east-1')
        png = io.BytesIO(screenshot)
        s3.upload_fileobj(png, 'daniascraper2', image_name)

    def get_urls(self):

        '''
        This function is used to retrieve URLs of recent instagram posts.
        '''

        username = "london"
        time.sleep(5)
        self.driver.get("https://www.instagram.com/" + username + "/")
        time.sleep(5)
        t_end = time.time() + 60 / 120
        instagram_urls = []
        i = 2
        while i > 0:
            for j in range(1, 2):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                posts = self.driver.find_elements(by=By.XPATH, value='//article[@class = "_aayp"]//div[@class = "_ac7v _aang"]//div[@class = "_aabd _aa8k _aanf"]/a')
                
                self.save_in_s3('urls.png')
                
                #os.environ["AWS_access_key"]
                #os.environ["AWS_secret_key"]

                for item in posts:
                    url=item.get_attribute("href")
                    instagram_urls.append(url)

            if(time.time() > t_end):
                break
        
        print("No. of urls in list", len(instagram_urls))
        a_set = set(instagram_urls)
        instagram_urls = list(a_set)
        print("Unique urls: ", len(instagram_urls))

        return instagram_urls

    def sort_by_date(self):

        '''
        This function is used to sort the URLs by date.
        '''

        #instagram_urls = ['https://www.instagram.com/p/CfW7ad2h29I/', 'https://www.instagram.com/p/CfZIJfmDKsO/']
        instagram_urls = self.get_urls()
        date_of_urls = []
        for c in instagram_urls:
            self.driver.get(c)
            p = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, './/time[@class = "_aaqe"]')))
            date_of_urls.append({"Date":p.get_attribute("title"), "url":c})
        
        date_df = pd.DataFrame(date_of_urls)
        print(date_df)
        date_df["Date"] = pd.to_datetime(date_df["Date"])
        date_df.sort_values(by='Date', ascending = False, inplace=True)
        date_df.drop('Date', inplace=True, axis=1)
        date_df = date_df[:3]
        print("No. of urls in final list: ", len(date_df))
        print(date_df)
        df = date_df.url.tolist()
        time.sleep(5)
        print("urls gotten")
        return df

    def create_uuids_for_url_list(self):

        '''
        This function is used to retrieve a unique UUID to assign to each of the URLs
        '''

        url = self.sort_by_date()
        ig_urls = [i.rsplit('/', 2)[-2] for i in url]
        uuid_list = [str(uuid4()) for x in ig_urls]
        dic = [str(x[0]) + '--' + x[1] for x in zip(ig_urls, uuid_list)]
        url_list = {'Unique Code':dic, 'url':url}
        df = pd.DataFrame(url_list)

        for column in df:
            s = df['url'].values
        s = list(s)
        return s

    def accept_cookies(self):

        '''
        This function is used to automatically accept cookies in the instagram webpage.
        '''

        self.save_in_s3('cookies.png')
        
        time.sleep(10)

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

        time.sleep(5)

    def scrape_comments(self):

        '''
        This function is used to scrape the comments from each of the posts.
        '''

        count = 0
        insta_urls = self.create_uuids_for_url_list()
        #insta_urls = ['https://www.instagram.com/p/CfW7ad2h29I/', 'https://www.instagram.com/p/CfZIJfmDKsO/']
        try:
            comments = []
            print("will now start scraping")
            for i in insta_urls:
                time.sleep(5)
                self.driver.get(i)

                self.save_in_s3('post.png')

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
                    comments.append({"url":i, "comments":elem.text})

        except Exception:
            print("program ended due to exception")
        print("no of values: ", len(comments))
        df = pd.DataFrame(comments)
        print("comments scraped")
        return df

    def perform_sentiment_analysis(self):

        '''
        This function is used to calculate the sentiments for all comments.
        '''
        
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

    def save_information(self):

        '''
        This function is used close a popup that appears after logging in.
        '''

        try:
            self.save_info = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Not now')]"))).click()
        except (TimeoutException, NoSuchElementException):
            pass

            time.sleep(5)
        
        try:
            self.turn_on_notifs = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
        except (TimeoutException, NoSuchElementException):
            pass

    def login(self):

        '''
        This function is used log in to the instagram account.
        '''

        sleep(2)

        username = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
        password = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
        username.clear()
        password.clear()
        username.send_keys(self.u)
        password.send_keys(self.p)
        log_in = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
        time.sleep(10)

        self.save_in_s3('login.png')

        print("logged in")

    def scrape_pictures(self):
        htmldata = urlopen("https://www.instagram.com/chantecaille/")
        soup = BeautifulSoup(htmldata, 'html.parser')
        images = soup.find_all('img')
        print(len(images))
        
        for item in images:
            i = item['src']
            image = i.replace("data:image/png;base64,", "")
            print(image)
            imgdata = base64.b64decode(image)
            print(type(imgdata))
            print(imgdata)

        with open("/Users/dq/Documents/dania_instagram_scraper/image.png", "wb") as fh:
            fh.write(imgdata)
        

    # def export_page_source(self, filepath : str):
    #     soup = self.driver.page_source
    #     soup = bs4.BeautifulSoup(soup,"html.parser")
    #     soup = str(soup.prettify)
        
    #     with open(f"/Users/dq/Documents/instagram_scraper/scraper_folder/{filepath}.txt", 'w') as f:
    #     # with open(f"{filepath}.txt", 'w') as f:
    #         f.write(soup)

if __name__ == "__main__":
    username = ['dummypracticetest4', 'dummypracticetest2', 'dummypracticetest3', 'dummypracticetest4']
    user = random.choice(username)
    s = Scraper(user, "dummy123456")
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

    insta_comments.to_sql('fm_scraping', engine, if_exists='append')