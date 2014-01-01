#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from abc import ABCMeta, abstractmethod

class AdCategoryCache(object):

	'''
    Category cache to hold all categorys, default method: load all category into memory
    
    Attributes:
    	ad_cs : list of ad category
    '''

	def __init__(self, ad_cs = []):
		self.ad_cs = ad_cs

	def push(self, ad_c):
		'''Load new category object

		Args:
			ad_c : new category object
		'''
		self.ad_cs.append(ad_c)

	def __iter__(self):  
	    return self.ad_cs


class AdCache(object):

	'''
    Abstract class, represent cache of ad
    '''    

	__metaclass__ = ABCMeta

	def __init__(self, ads = []):
		pass

	@abstractmethod
	def push(self, ad):
		'''Load new ad object

		Args:
			ad : ad object
		'''
		pass

	@abstractmethod
	def get_ads(self, ad_c):
		'''Get all ad belong to the ad category

		Args:
			ad_c : the ad category

		Returns:
			list of ads
		'''
		pass


class DefalutAdCache(AdCache):

	'''
    Ad cache to hold all ads, default method: load all category into memory
    
    Attributes:
    	cache : list of ad
    '''

	def __init__(self, ads = []):
		self.cache = ads

	def push(self, ad):
		self.cache.append(ad)

	def get_ads(self, ad_c):
		res = []
		for ad in self.cache:
			if ad.ad_c == ad_c:
				res.append(ad)
		return res

	def __iter__(self):  
		return self.cache.__iter__()


class AdCacheWithCategory(AdCache):

	'''
    Ad cache to hold all ads use category as key, default method: load all category into memory
    
    Attributes:
    	cache : {ad_c : [ads]}
    '''

	def __init__(self, ads = []):
		self.cache = {}
		for ad in ads:
			try:
				self.cache[ad.ad_c].append(ad)
			except:
				self.cache[ad.ad_c] = [ad]

	def push(self, ad):
		try:
			self.cache[ad.ad_c].append(ad)
		except:
			self.cache[ad.ad_c] = [ad]

	def get_ads(self, ad_c):
		try:
			return self.cache[ad_c]
		except:
			return []

	def __iter__(self):  
		res = []
		for ads in self.cache.values():
			res += ads
		return res.__iter__()