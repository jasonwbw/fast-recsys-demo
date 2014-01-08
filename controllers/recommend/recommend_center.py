#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

import ConfigParser
from tools import builder, distance
from bean import loader
from ranking.ranking_strategys import Ranking
from retrival.category_retrival_strategys import CategoryRetrivalStrategyCenter
from abc import ABCMeta, abstractmethod

class ChooseController(object):

	'''Used for demo, other demo can extends this class
	'''

	__metaclass__ = ABCMeta

	@abstractmethod
	def __init__(self, **args):
		pass

	@abstractmethod
	def load_conf(self):
		'''Read config file and build builder, distance and loader'''
		pass

	@abstractmethod
	def build_vec_getter(self):
		'''Build the ad and content vector getter
		
		Returns:
			tuple of ad vector getter and content vector getter
		'''
		pass

	@abstractmethod
	def number_content(self):
		'''Give all content number and save the key'''
		pass

	@abstractmethod
	def content_count(self):
		'''Count the content number

		Returns:
			the result number
		'''
		pass

	@abstractmethod
	def get_content_ads(self, num):
		'''Get the content whose id is num and the recommend ads

		Args:
			num : content id

		Returns:
			(content, [list of ad content])
		'''
		pass


class RankingChooseController(ChooseController):

	'''Just use the ranking process.
	'''

	def __init__(self):
		self.load_conf()
		getters = self.build_vec_getter()

		self.ranking = Ranking(self.builder, self.distance, getters[0], getters[1])
		self.ad_cache = self.loader.load_ads()[1]

		self.number_content()

	def load_conf(self):
		'''Read config file and build builder, distance and loader'''
		cf = ConfigParser.RawConfigParser(allow_no_value=True)
		
		import os
		paths = ['controllers', 'recommend', 'controller.cfg']
		_file = os.getcwd()
		for path in paths:
			_file = os.path.join(_file, path)
		with open(_file,'r') as configfile:       
			cf.readfp(configfile)	

		builder_class = cf.get("class", 'builder')
		builder_args = eval(cf.get("args", 'builder'))
		self.builder = getattr(builder, builder_class)(args = builder_args)
		
		distance_class = cf.get("class", 'distance')
		distance_args = eval(cf.get("args", 'distance'))
		self.distance = getattr(distance, distance_class)(args = distance_args)
		
		loader_class = cf.get("class", 'loader')
		loader_args = eval(cf.get("args", 'loader'))
		self.loader = getattr(loader, loader_class)(args = loader_args)

	def build_vec_getter(self):
		'''Build the ad and content vector getter
		
		Returns:
			tuple of ad vector getter and content vector getter
		'''
		ad_vec_getter = lambda vec : vec.get_vec()
		content_vec_getter = lambda vec : vec.get_vec()
		return (ad_vec_getter, content_vec_getter)

	def number_content(self):
		'''Give all content number and save the key'''
		self.count = 8
		self.content_key = { 0 : {'category' : 'IT', 'file' : '10.txt'},
		                     1 : {'category' : 'IT', 'file' : '11.txt'},
		                     2 : {'category' : 'IT', 'file' : '18.txt'},
		                     3 : {'category' : '体育', 'file' : '12.txt'},
		                     4 : {'category' : '体育', 'file' : '13.txt'},
		                     5 : {'category' : '体育', 'file' : '14.txt'},
		                     6 : {'category' : '体育', 'file' : '16.txt'},
		                     7 : {'category' : '体育', 'file' : '17.txt'}
		                    }

	def content_count(self):
		return self.count

	def get_content_ads(self, num):
		'''Get the content whose id is num and the recommend ads

		Args:
			num : content id

		Returns:
			(content, [list of ad content])
		'''
		if num >= self.count:
			return None
		content_obj = self.loader.load_content(self.content_key[num])
		ads = self.ranking.ranking(content_obj, self.ad_cache, topk = 2)
		res_ad = []
		for score, ad_key in ads:
			res_ad.append(self.loader.get_ad_info(ad_key))
		return (self.loader.get_content_info(self.content_key[num]), res_ad)


class RetrivalAndRankingChooseController(RankingChooseController):

	'''Use the retrival ad category firstly, and ranking the ads.
	'''

	def __init__(self):
		self.load_conf()
		getters = self.build_vec_getter()

		self.ranking = Ranking(self.builder, self.distance, getters[0], getters[1])
		self.ad_c_cache, self.ad_cache = self.loader.load_ads()

		self.number_content()
		self.retrival = CategoryRetrivalStrategyCenter(builder = self.builder, distance = self.distance)

	def get_content_ads(self, num):
		'''Get the content whose id is num and the recommend ads

		Args:
			num : content id

		Returns:
			(content, [list of ad content])
		'''
		if num >= self.count:
			return None
		content_obj = self.loader.load_content(self.content_key[num])
		
		categorys = self.retrival.get_category(content_obj, self.ad_c_cache)
		retrival_ads = []
		for category in categorys:
			retrival_ads += self.ad_cache.get_ads(category)
		print retrival_ads
		
		ads = self.ranking.ranking(content_obj, retrival_ads, topk = 2)
		res_ad = []
		for score, ad_key in ads:
			res_ad.append(self.loader.get_ad_info(ad_key))
		return (self.loader.get_content_info(self.content_key[num]), res_ad)