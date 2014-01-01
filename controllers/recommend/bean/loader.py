#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from abc import ABCMeta, abstractmethod
import ConfigParser
import os
import linecache

class Loader(object):

	'''
    Abstract class, define the interface for ad and content loader
    '''   

	__metaclass__ = ABCMeta

	def __init__(self, **args):
		pass

	@abstractmethod
	def get_ad_info(self, key):
		'''Get the ad info 

		Args:
			key : the ad's key

		Returns:
			info dictionary
		'''
		pass

	@abstractmethod
	def get_content_info(self, key):
		'''
		Get the content info 

		Args:
			key : the content's key

		Returns:
			info dictionary
		'''
		pass

	@abstractmethod
	def load_ads(self, **args):
		'''Load all ads into ad cache

		Args:
			args : info like db or file for subclass to build the obj

		Returns:
			(ad_c_cache, ad_cache)
		'''
		pass

	@abstractmethod
	def load_content(self, key):
		'''Load the content object by the given info

		Args:
			key : the given info

		Returns:
			the content object
		'''
		pass

	@abstractmethod
	def random_content(self):
		'''Random a content object

		Returns:
			the content object
		'''
		pass


class DemoLoader(Loader):

	'''
	Loader's implementation class for demo data
	'''

	def __init__(self, **args):
		cf = ConfigParser.RawConfigParser(allow_no_value=True)

		paths = ['controllers', 'recommend', 'bean', 'loader.cfg']
		_file = os.getcwd()
		for path in paths:
			_file = os.path.join(_file, path)
		with open(_file,'r') as configfile:       
			cf.readfp(configfile)	

		self.content_folder = cf.get('demo', 'content_folder')
		self.content_vec_folder =  cf.get('demo', 'content_vec_folder')
		self.ad_file = cf.get('demo', 'ad_file')
		self.ad_vec_file = cf.get('demo', 'ad_vec_file')
		self.ad_c_vec_file = cf.get('demo', 'ad_c_vec_file')

	def get_ad_info(self, key):
		return linecache.getline(self.ad_file, key).strip()

	def get_content_info(self, key):
		category = key['category']
		file_num = key['file']
		content = ''
		with open(os.path.join(os.path.join(self.content_folder, category), file_num), 'r') as fp:
			for line in fp:
				content = content + line.strip() + ' '
		return (category, content)

	def load_ads(self, **args):
		from ..bean.ad_cache import DefalutAdCache
		from ..bean.ad import DefaultAd
		from ..bean.ad import AdCategory

		ad_cache = DefalutAdCache()
		with open(self.ad_vec_file, 'r') as fp:
			linecache_num = 0
			for line in fp:
				linecache_num += 1
				category, words = line.strip().split(':')
				ad_c = AdCategory(category)
				ad = DefaultAd(linecache_num, ad_c, title = words)
				ad_cache.push(ad)
		return (None, ad_cache)

	def load_content(self, key):
		from ..bean.content import TfContent

		category = key['category']
		file_num = key['file']
		content = ''
		with open(os.path.join(os.path.join(self.content_vec_folder, category), file_num), 'r') as fp:
			for line in fp:
				content = content + line.strip() + ' '
		return TfContent(category = category, content = content)

	def random_content(self):
		pass