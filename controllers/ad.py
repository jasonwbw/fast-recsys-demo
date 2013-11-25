#!/usr/bin/env python
# coding: utf-8

import web
from config import settings

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

render = settings.render

class ContentIndex:
    def GET(self):       
        content_title, content_text = self._get_content()
        rec_total, recs, other_info = self._get_rec(content_title, content_text)
        feedback_url = "./"
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
    def POST(self, title, recid, message):   
    	pass