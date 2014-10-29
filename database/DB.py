import sys
from mysql.connector import errorcode
import mysql.connector as mdb
from datetime import datetime, timedelta, date
import collections
import simplejson as json
import tweepy
from tweepy.utils import import_simplejson


DB_NAME = 'Twit'
add_data=" "

con=mdb.connect(user='root',password='12345678',database=DB_NAME);

cursor = con.cursor()


TABLES = {}
TABLES['Twitter'] = (
    "CREATE TABLE `Twitter` ("
    "  `user` BIGINT NOT NULL AUTO_INCREMENT,"
    "  `tid` BIGINT NOT NULL DEFAULT 12345678,"
    "  `lat` FLOAT(10,6) NOT NULL DEFAULT 0,"
    "  `lon` FLOAT(10,6) NOT NULL DEFAULT 0,"
    "  `text` VARBINARY(255)  NOT NULL DEFAULT 'blank',"
    "  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "  `kwd` VARCHAR(20) NOT NULL DEFAULT 'coffee',"
    "  PRIMARY KEY (`user`)"
    ") ENGINE=InnoDB")


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mdb.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    con.database = DB_NAME    
except mdb.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        con.database = DB_NAME
    else:
        print(err)
        exit(1)

for name, ddl in TABLES.iteritems():
    try:
        print("Creating table {}: ",format(name))
        cursor.execute(ddl)
    except mdb.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

#authorize tweepy api
CONSUMER_KEY = 'wfg76HPo6k56ItgdRCepxAvch'
CONSUMER_SECRET = 'xn6PZNNO7ieGQgHfcuuAUiCTZMJtnExgtWyXcJK1G1EbssloXx'
ACCESS_TOKEN_KEY = '43335008-tl7cFjjCOgEEukxlMBt1izBjKjKxrFIEfinonvohm'
ACCESS_TOKEN_SECRET = 'YF3IZM5Xr7o8PkMZai6lHCTeNwbsEkWY7WrUUpQY3Iaxi'


auth1 = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth1.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

#This class holds the tweet - it's structured 
# on purpose so we can easily access elements in
# a template tag
class tweet():
    def __init__(self, user,tid, text, geo, time,kwd):
        self.user = user
        self.text = text
        self.geo = geo
        self.time = time
        self.tid = tid
        self.kwd = kwd


def search_twitter(data):   
  #  js = data.readlines()
    js_object = json.loads(data)
    
    #filter it all
    tweets = []
    kwd = 'coffee'
    try:
        user = js_object['id']
        tid = js_object['user']['id']
        geo = js_object['coordinates']
        text = js_object['text']
        ts = js_object['created_at']      
        time = datetime.strptime(js_object['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
    except KeyError:
        return None
    
    thistweet = tweet(user,tid, text, geo, time, kwd)
    tweets.append(thistweet)
    if thistweet.geo is not None and thistweet.text is not None and thistweet.tid is not None and thistweet.time is not None and thistweet.user is not None:
        global add_data
        print data
        print thistweet.user
        print thistweet.tid
        print thistweet.geo
        print thistweet.geo['coordinates'][1]
        print thistweet.geo['coordinates'][0]
        print type(thistweet.geo['coordinates'][0])
        print thistweet.text
        print thistweet.time
        
        add_data = ("INSERT INTO Twitter "
              "(user,tid, lat, lon, text, time, kwd) "
               "VALUES (%(user)s, %(tid)s, %(lat)s,%(lon)s, %(text)s, %(time)s, %(kwd)s)")
        data_set = {
                       'user': thistweet.user,
                       'tid': thistweet.tid,
                       'lat': thistweet.geo['coordinates'][0],
                       'lon': thistweet.geo['coordinates'][1],
                       'text': thistweet.text,
                       'time': thistweet.time,
                       'kwd': kwd,
                       }
     
        cursor.execute(add_data, data_set)
        twit_no = cursor.lastrowid
        print twit_no
        print("Getting table {}: ",format(name),twit_no)
        
        con.commit()
        return tweets 
    else:
        pass

class StreamListener(tweepy.StreamListener):
    
    def on_status(self, tweet):
        print 'Ran on_status'

    def on_error(self, status_code):
        return False

    def on_data(self, data):
        if not data[0].isdigit():
            tws=search_twitter(data) 
l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l)
setTerms = ['coffee']
streamer.filter(track = setTerms)
