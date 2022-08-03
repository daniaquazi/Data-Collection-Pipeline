from scraper import Scraper
import boto3
import json
import pandas as pd
import ast
import re
import boto3
from sqlalchemy import create_engine
import psycopg2
# def main():
# s = Scraper("dummypracticetest", "dummy12345")
# s.accept_cookies()
# s.login()
# s.save_information()
# s.scrape_comments()
# file_name = "/Users/dq/Documents/savesss_output.txt"
# s.dump_products(file_name)

# s3 = boto3.client('s3')
# bucket = s3.create_bucket(Bucket='daniawebscraper', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
# s3 = boto3.resource('s3')
# s3.meta.client.upload_file('/Users/dq/Documents/savesss_output.txt', 'daniawebscraper', 'savesss_output.txt')

with open("/Users/dq/Documents/savesss_output.txt", "r") as f:
    data = f.read().replace('"",', '",\n"')
data = "["+data+"]"
data = ast.literal_eval(data)
df = pd.DataFrame (data, columns = ['comments'])

data_cleaning_comments = lambda x: re.sub("([^0-9A-Za-z'])"," ",x)
df["comments"] = df.comments.map(data_cleaning_comments)
print(df)


    # s.driver.get("https://google.com/")
    # l = ["CeOhA1vtSAR", "CeOFMd3NkDE", "CeNsJ_6NTJ_/"]
    # for i in l:
    #     s.scrape_comments(i)

    #bot = Scraper("www.instagram.com")

# if __name__ == "__main__":
#     main()

from sqlalchemy import create_engine
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'igcomments.ceksj31rldpd.us-east-1.rds.amazonaws.com'
USER = 'postgres'
PASSWORD = 'rdsdatabasepassword'
PORT = 5432
DATABASE = 'postgres'
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
engine.connect()

df.to_sql('ig_comments', engine, if_exists='replace')