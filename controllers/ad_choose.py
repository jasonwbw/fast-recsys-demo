#!/usr/bin/env python
# coding: utf-8

import web
from config import settings
from recommend.recommend_center import ChooseController
from abc import ABCMeta, abstractmethod

render = settings.render

# global attribute
controller = ChooseController()

class AbstractContentIndex:

    __metaclass__ = ABCMeta

    @abstractmethod
    def __get_content(self, **args):
        '''Get the content's title and detail text

        Returns:
            content_title, content_text
        '''
        pass

    @abstractmethod
    def _get_rec(self, **args):
        '''Get the recommend result

        Returns:
            total information, recs, other information
            (recs is [{'text':*, 'img':*}], if len(recs)%3 is not 0, the add enough empty element to recs.)
        '''

class ContentIndex(AbstractContentIndex): 

    def GET(self, page = None):
        global controller
        page_num = page and int(page) or 0
        content, ads = controller.get_content_ads(page_num)
        content_title, content_text = self._get_content(content = content)
        rec_total, recs, other_info = self._get_rec(ads = ads)
        feedback_url = "./feedback_base_ad"
        item_contain_img = False
        return render.ads_choose(page_num, content_title, content_text,\
        	rec_total, recs, \
        	other_info, feedback_url, item_contain_img)

    def _get_content(self, **args):
    	content = args['content']
        content_title = content[0]
        content_text = content[1]
        return content_title, content_text

    def _get_rec(self, **args):
    	rec_total = ""
        recs = []
        for rec in args['ads']:
            recs.append({'text' : rec, 'img' : ''})
        for i in xrange(3 - len(recs) % 3):
            recs.append({'text' : '', 'img' : ''})
        other_info = "no other info"
        return rec_total, recs, other_info

class Feedback:

    def POST(self):   
        data = web.input()
        self.handle_feedback_data(data)

    def handle_feedback_data(self, data):
    	return 'feed back', 'title:', data['title'], ', recid:', data['recid'], ', message:', data['message']