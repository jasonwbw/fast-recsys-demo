#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from abc import ABCMeta, abstractmethod
from numpy.linalg import norm

class Distance(object):
	
	'''
    Abstract class, represent distance of two dictionary
    '''

	__metaclass__ = ABCMeta

	def __init__(self, **args):
		pass

	@abstractmethod
	def distance(self, vec1, vec2):
		'''Compute distance of two dictionary

		Args:
			vec1: the first line vector, an instance of array
        	vec2: the second line vector, an instance of array

        Returns:
        	the computed distance
        ''' 
        pass


class CosineDistance(Distance):
	
	'''
	Cosine distance of two dictionary
	'''

	def distance(self, vec1, vec2):
		if len(vec1) == 0 or len(vec2) == 0:
			return 0
		big = len(vec1) > len(vec2) and vec2 or vec1
		small = len(vec1) > len(vec2) and vec1 or vec2
		dot = 0.0
		for word, value in small.items():
			if word in big:
				dot += value * big[word]
		return dot / (norm(vec1.values()) * norm(vec2.values()))