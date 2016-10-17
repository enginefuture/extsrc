# -*- coding: utf-8 -*-
import feedparser
import json
import urllib2
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)

WEATHER_API = "7ec1954dea399366ca23e3c8d2216e97"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=%s" % WEATHER_API
CURRENCY_API = "ad85ef735e2240afa614cf7698eeeb01"
CURRENCY_URL = 'https://openexchangerates.org//api/latest.json?app_id=%s' % CURRENCY_API

DEFAULTS = {'publication':'zhihu',
            'city':'Hefei,CN',
            'currency_from':'GBP',
            'currency_to':'USD'}

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'zhihu':'http://rss.sina.com.cn/roll/mil/hot_roll.xml'}

@app.route('/')
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate = get_rate(currency_from,currency_to)
    return render_template('home.html',articles=articles,
                           weather=weather,currency_from=currency_from,
                           currency_to=currency_to,rate=rate)

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    # first_article = feed['entries'][0]
    return feed['entries']

def get_weather(query):
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {
            "description":parsed["weather"][0]["description"],
            "temperature":parsed["main"]["temp"],
            "city":parsed["name"],
            "country":parsed["sys"]['country']
        }
    return weather

def get_rate(frm,to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return to_rate/frm_rate


if __name__ == '__main__':
    app.run(port=5000,debug=True)
