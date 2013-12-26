#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from abc import ABCMeta, abstractmethod

class Content(object):

	'''
    Abstract class, represent the content
    
    Attributes:
    	category : the news category, seged data
    	category_extend : the words extended for category, list of words
    	title : the content title, seged data
    	content : the content text, seged data
    '''    

    __metaclass__ = ABCMeta

	def __init__(self, category = None, category_extend = [] title = None, content = None, **args):
		self.category = category
		self.category_extend = category_extend
		self.title = title
		self.content = content

	@abstractmethod
	def get_contentc_vec(self, need_extend = False):
		'''Get the vector of category

		Args:
			need_extend : need the extend info or not

		Returns:
			the vector represent this content's category
		'''
		pass

	@abstractmethod
	def get_vec(self):
		'''Get the content vector

		Returns:
			the vector represent this content
		'''
		pass

class DefaultContent(Content):

	'''
	Default implementation class. Return the vector contain all info's words
	'''

	def get_contentc_vec(self, need_extend = False):
		res = []
		if self.category:
			res += self.category.split()
		if need_extend and self.category_extend:
			res += self.category_extend
		return res

	def get_vec(self):
		res = []
		if self.title:
			res += self.title.split()
		if self.content:
			res += self.content.split()
		return res


class TfAd(Ad):
	'''
	Content's implementation class to return the vector contain words in title/content with df
	'''

	def get_contentc_vec(self, need_extend = False):
		res = {}
		if self.category:
			for term in self.category.split():
				try:
					res[term] += 1
				except:
					res[term] = 1 
		if need_extend and self.category_extend:
			for term in self.category_extend:
				try:
					res[term] += 1
				except:
					res[term] = 1 
		return res.items()

	def get_vec(self):
		words = []
		if self.title:
			words += self.title.split()
		if self.content:
			words += self.content.split())
		res = {}
		for term in words:
			try:
				res[term] += 1
			except:
				res[term] = 1
		return res.items()