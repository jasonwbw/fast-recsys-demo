#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

class AdCategoryCache(object):

	'''
    Category cache to hold all categorys, default method: load all category into memory
    
    Attributes:
    	ad_cs : list of ad category
    '''

	def __init__(self, ad_cs):
		self.ad_cs = ad_cs

	def add_ad_c(self, ad_c):
		'''Load new category object

		Args:
			ad_c : new category object
		'''
		self.ad_cs.append(ad_c)

	def __iter__(self):  
	    return self.ad_cs


class AdCache(object):

	'''
    Ad cache to hold all ads, default method: load all category into memory
    
    Attributes:
    	ad_s : list of ad
    '''

	def __init__(self, ads):
		self.cache = {}
		for ad in ads:
			try:
				self.cache[ad.ad_c].append(ad)
			except:
				self.cache[ad.ad_c] = [ad]

	def add_ad(self, ad):
		'''Load new ad object

		Args:
			ad : ad object
		'''
		try:
			self.cache[ad.ad_c].append(ad)
		except:
			self.cache[ad.ad_c] = [ad]

	def get_ads(self, ad_c):
		'''Get all ad belong to the ad category

		Args:
			ad_c : the ad category

		Returns:
			list of ads
		'''
		try:
			return self.cache[ad_c]
		except:
			return []

	def __iter__(self):  
		res = []
		for ads in self.cache.values():
			res += ads
	    return res