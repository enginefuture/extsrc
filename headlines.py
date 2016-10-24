# -*- coding: utf-8 -*-
from flask import Flask
from flask import make_response
from flask import render_template
from flask import request
import datetime
import feedparser
import json
import sys
import urllib
import urllib2
reload(sys)
sys.setdefaultencoding('utf-8')


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
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)
    city = get_value_with_fallback('city')
    weather = get_weather(city)
    currency_from = get_value_with_fallback('currency_from')
    currency_to = get_value_with_fallback('currency_to')
    rate, currencies = get_rate(currency_from,currency_to)
    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             currency_to=currency_to,
                                             currency_from=currency_from,
                                             rate=rate,
                                             currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication",publication,expires=expires)
    response.set_cookie("city",city,expires=expires)
    response.set_cookie("currency_from",currency_from,expires=expires)
    response.set_cookie("currency_to",currency_to,expires=expires)
    return response

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

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
    return (to_rate/frm_rate, parsed.keys())


if __name__ == '__main__':
    app.run(port=5000,debug=True)
