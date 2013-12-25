#!/usr/bin/env python
# coding: utf-8

import web
from config import settings

import os
import random
import linecache
from lib.ads import ADs
from lib.buildvec_online import VecBuilderOnline

render = settings.render

# global attribute
base = '/home/adrd-dev/nlp_flow/code'
builder = VecBuilderOnline(base + "/data/idf", base + "/data/pairs", \
    base + "/data/kw", base + "/data/kw_pmi_app", base + "/data/kw_w2v_app")
ads = ADs(base + '/all_ad_c_vec', \
    base + '/all_ad_vec')
basepath = base + '/data/output/'
segedbasepath = base + '/seged/output/'

class ContentIndex: 

    def GET(self):
        global builder
        news_c = random.choice(builder.all_news_c())
        line = random.randint(1, 50)
        content_title, content_text = self._get_content(attrs = {'news_c':news_c, 'line':line})
        rec_total, recs, other_info = self._get_rec(attrs = {'news_c':news_c, 'line':line})
        feedback_url = "./feedback_base_ad"
        return render.index(content_title, content_text,\
        	rec_total, recs, \
        	other_info, feedback_url)

    def _get_content(self, attrs = None):
        global basepath
    	content_title = attrs['news_c']
        content_text = linecache.getline(basepath+attrs['news_c']+'/news', attrs['line'])
        return content_title, content_text

    def _get_rec(self, attrs = None):
        global basepath, segedbasepath, builder, ads
        news = linecache.getline(segedbasepath+attrs['news_c']+'/news', attrs['line'])
        vec = builder.build_news_tfidf(attrs['news_c'], news.split(" "))
        items = ads.find_ad(2, 5, vec, attrs['news_c'])
    	rec_total = ""
        recs = []
        for ad_c, item in items:
            rec_total += ad_c + " "
            recs.append({'text': linecache.getline(basepath+attrs['news_c']+'/'+ad_c, int(item)).strip(), \
                "img":" "})
        other_info = "no other info"
        return rec_total, recs, other_info

class Feedback:

    def POST(self):   
        data = web.input()
        self.handle_feedback_data(data)

    def handle_feedback_data(self, data):
    	return 'feed back', 'title:', data['title'], ', recid:', data['recid'], ', message:', data['message']