#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from abc import ABCMeta, abstractmethod

class Content(object):

	'''
    Abstract class, represent the content
    
    Attributes:
    	title : the content title
    	content : the content text
    '''    

    __metaclass__ = ABCMeta

	def __init__(self, category = None, title = None, content = None, **args):
		self.category = category
		self.title = title
		self.content = content

	@abstractmethod
	def get_contentc_vec(self):
		'''Get the vectory of category

		Returns:
			the vectory represent this content's category
		'''
		pass

	@abstractmethod
	def get_vec(self):
		'''Get the content vectory

		Returns:
			the vectory represent this content
		'''
		pass

class DefaultContent(Content):

	'''
	Default implementation class. Return the vectory contain all info's words
	'''

	def get_contentc_vec(self):
		res = []
		if self.category:
			res += self.category.split()
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
	Content's implementation class to return the vectory contain words in title/content with df
	'''

	def get_contentc_vec(self):
		res = {}
		if self.category:
			for term in self.category.split():
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