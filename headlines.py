# -*- coding: utf-8 -*-
import feedparser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask
from flask import render_template

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'zhihu':'http://rss.sina.com.cn/roll/mil/hot_roll.xml'}

@app.route('/')
@app.route('/<publication>')
def get_news(publication='bbc'):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=5000,debug=True)