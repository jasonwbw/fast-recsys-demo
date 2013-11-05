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
        return render.index("test_title", "test_content", "recommend total", \
                            [{'text':"text1","img":"images/pic06.jpg"}, {'text':"text2","img":"images/pic06.jpg"}, \
                             {'text':"text3","img":"images/pic06.jpg"}, {'text':"text4","img":"images/pic06.jpg"}], \
                            "no other info", "http://demo")