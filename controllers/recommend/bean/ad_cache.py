#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

class AdCategoryCache(object):

	def __init__(self, ad_cs):
		self.ad_cs = ad_cs

	def add_ad_c(self, ad_c):
		self.ad_cs.append(ad_c)

	def __iter__(self):  
	    return self.ad_cs


class AdCache(object):

	def __init__(self, ads):
		self.cache = {}
		for ad in ads:
			try:
				self.cache[ad.ad_c].append(ad)
			except:
				self.cache[ad.ad_c] = [ad]

	def get_ads(self, ad_c):
		try:
			return self.cache[ad_c]
		except:
			return []