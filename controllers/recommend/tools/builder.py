#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from abc import ABCMeta, abstractmethod
import math

class VecBuilder(object):
	
	'''
    Abstract class, represent the content
    
    Attributes:
    	title : the content title
    	content : the content text
    '''

	__metaclass__ = ABCMeta

	def __init__(self, **args):
		pass

	@abstractmethod
	def get_vec(self, vec):
		'''Get the final vector to compute

		Args:
			vec : the word vec

		Returns:
			the dictionary
		'''
		pass


class DefaultVecBuilder(object):

	'''
    Default implementation class. Return the vector contain all terms with same value
    '''    

	def get_vec(self, vec):
		res = {}
		def_value = 1
		for term in vec:
			res[term] = 1
		return res


class TfidfVecBuilder(object):

	'''
	Tfidf value for all terms.

	Attributes:
		dfs : all {word : df value}
		total : total number of doc
	'''

	def __init__(self, **args):
		self.dfs =  args['dfs']
		self.total = args['total']

	def get_vec(self, vec):
		'''Build the tf-idf vector

		Args:
			vec : the word vec with tuple (term, tf)
		'''
		res = {}
		for term, tf in vec:
			try:
				idf = math.log(float(1.0 + self.total) / (1 + self.dfs[term]))
				res[term] = tf * idf
			except KeyError:
				pass
		return res