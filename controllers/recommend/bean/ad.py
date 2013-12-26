#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from abc import ABCMeta, abstractmethod
import copy

class AdCategory(object):

	'''
    Represent the ad category
    
    Attributes:
    	name : the category name
    	keywords : the keywords of this category
    	extend_keywords : the extended keywords by topic model or other method
    '''    

	def __init__(self, name, keywords = [], extend_keywords = []):
		self.name = name
		self.keywords = keywords
		self.extend_keywords = extend_keywords

	def get_vec(self, needkeywords = False, need_extend_keywords = False):
		'''Get the vector of category

		Args:
			needkeywords : need category keywords or not for vector
			need_extend_keywords ：need extended category keywords or not for vector

		Returns:
			the vector represent this category
		'''
		res = [self.name]
		if needkeywords:
			res += self.keywords
		if need_extend_keywords:
			res += self.extend_keywords
		return res


class Ad(object):

	'''
    Abstract class, represent the ad
    
    Attributes:
    	ad_c : an instance of AdCategory
    	keywords : the keywords of this ad
    	title : the ad title
    	content : the ad content
    '''    

	__metaclass__ = ABCMeta

	def __init__(self, ad_c, keywords = [], title = None, content = None):
		self.ad_c = ad_c
		self.keywords = keywords
		self.title = title
		self.content = content

	def get_adc_vec(self, needkeywords = False, need_extend_keywords = False):
		'''Get the vector of category

		Args:
			needkeywords : need category keywords or not for vector
			need_extend_keywords ：need extended category keywords or not for vector

		Returns:
			the vector represent this ad's category
		'''
		return self.ad_c.get_vec(needkeywords = needkeywords, need_extend_keywords = need_extend_keywords)

	@abstractmethod
	def get_vec(self, needcontent = True):
		'''Get the ad vector]

		Args:
			needcontent : need title and content or not, if not just use keywords
		Returns:
			the vector represent this content
		'''
		pass


class DefaultAd(Ad):

	'''
	Default implementation class. Return the vector contain words in keywords/title/content
	'''

	def get_vec(self, needcontent = True):
		res = copy.copy(self.keywords)
		if needcontent and self.title != '':
			res += self.title.split()
		if needcontent and self.content != '':
			res += self.content.split())
		return res


class TfAd(Ad):

	'''
	Ad's implementation class to return the vector contain words in keywords/title/content with df
	'''

	def get_vec(self, needcontent = True):
		words = copy.copy(self.keywords)
		if needcontent and self.title != '':
			words += self.title.split()
		if needcontent and self.content != '':
			words += self.content.split())
		res = {}
		for term in words:
			try:
				res[term] += 1
			except:
				res[term] = 1
		return res.items()