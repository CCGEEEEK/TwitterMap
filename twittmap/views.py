from django.shortcuts import render
from twittmap.models import Tweet
from django.http import HttpResponse

DB_NAME = 'Twit'

def book_list(request):
    #db = mdb.connect(user='root',password='12345678',database=DB_NAME);
    #cursor = db.cursor()
 
    tweet = Tweet()
    tweet.lat = Tweet.objects().get('lat')
    tweet.lon = Tweet.objects().get('lon')
   # cursor.execute('SELECT name FROM books ORDER BY name')
    return HttpResponse('<h1>OK</h1>')