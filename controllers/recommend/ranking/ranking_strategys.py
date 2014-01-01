#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from ..tools.topkheap import TopkHeap

class Ranking(object):

	'''
    Represent the ranking strategy

    Attributes:
    	builder : ..tools.builder.Builder object for builder the dictionary for vector
    	distance : ..tools.distance.Distance object for compute the distance of two vector
    	ad_vec_getter : the method to get the vec for ..bean.ad.Ad object
    	content_vec_getter : the method to get the vec for ..bean.content.Content object
    '''    

	def __init__(self, builder, distance, ad_vec_getter, content_vec_getter, **args):
		self.builder = builder
		self.distance = distance
		self.ad_vec_getter = ad_vec_getter
		self.content_vec_getter = content_vec_getter

	def ranking(self, content, ad_cache, topk = None):
		'''Rank all ads based on content

		Args:
			content : the content.Content object
			ad_cache : the ad_cache.AdCache object
			topk : top k ranking element

    	        Returns:
		        list of (ad.key, rank)
		'''
		vec_content = self.builder.get_vec(self.content_vec_getter(content))
		if topk != 0:
			heap = TopkHeap(topk)
			for ad in ad_cache:
				heap.push((self.distance.distance(self.builder.get_vec(self.ad_vec_getter(ad)), vec_content), ad.key))
			return heap.topk()
		else:
			heap = []
			for ad in ad_cache:
				heap.append((self.distance.distance(self.builder.get_vec(self.ad_vec_getter(ad)), vec_content), ad.key))
			return sorted(heap)[::-1]


if __name__ == '__main__':
	center = Ranking()