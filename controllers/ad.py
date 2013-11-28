#!/usr/bin/env python
# coding: utf-8

import web
from config import settings

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

render = settings.render

# global attribute
_id = 1

class ContentIndex: 

    def GET(self):
        global _id
        _id += 1
        print '_id' + str(_id)
        content_title, content_text = self._get_content()
        rec_total, recs, other_info = self._get_rec(content_title, content_text)
        feedback_url = "./feedback_base_ad"
        return render.index(content_title, content_text,\
        	rec_total, recs, \
        	other_info, feedback_url)

    def _get_content(self):
    	content_title = "test_title" 
        content_text = "test_content"
        return content_title, content_text

    def _get_rec(self, content_title, content_text):
    	rec_total = "recommend total"
        recs = [{'text':"text1","img":"images/pic06.jpg"}, {'text':"text2","img":"images/pic06.jpg"}, \
                {'text':"text3","img":"images/pic06.jpg"}, {'text':"text4","img":"images/pic06.jpg"}]
        other_info = "no other info"
        return rec_total, recs, other_info

class Feedback:

    def POST(self):   
        data = web.input()
    	return 'feed back', 'title:', data['title'], ', recid:', data['recid'], ', message:', data['message']