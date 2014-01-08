#!/usr/bin/env python
# coding: utf-8
#
# @author: Jason Wu (Jasonwbw@yahoo.com)

from abc import ABCMeta, abstractmethod
import ConfigParser
import sys

thismodule = sys.modules[__name__]

class CategoryRetrivalStrategyCenter(object):

	'''
    Pipeline control center for retrival ad categorys.

    Attribute:
    	pipelines : the pipelines queue
    	builder : ..tools.builder.Builder object for builder the dictionary for vector
    	distance : ..tools.distance.Distance object for compute the distance of two vector
    	ad_c_vec_getter : the method to get the vec for ..bean.ad.AdCategory object
    	content_vec_getter : the method to get the vec for ..bean.content.Content object
    '''  

	def __init__(self, builder, distance, ad_c_vec_getter, content_vec_getter):
		self.pipelines = []
		cf = ConfigParser.ConfigParser()

		import os
		paths = ['controllers', 'recommend', 'retrival', 'strategys.cfg']
		_file = os.getcwd()
		for path in paths:
			_file = os.path.join(_file, path)
		with open(_file,'r') as configfile:       
			cf.readfp(configfile)	

		options = cf.options("pipeline")
		global thismodule
		for option in options:
			args = eval(cf.get("args", option))
			_class = cf.get("pipeline", option)
			tmp_pipeline = getattr(thismodule, _class)(builder, distance, ad_c_vec_getter, content_vec_getter, args = args)
			self.pipelines.append(tmp_pipeline)

	def get_category(self, content, adc_cache):
		'''Use the pipeline design pattern. 
		Handle the retrival by the certain pipeline in pipelines queue.
		The pass with continue when pipeline element return an empty list. Otherwise, return the result.

		Args:
			content : the content.Content object
			adc_cache : the ad_cache.AdCategoryCache object

		Returns:
			the list of ad.AdCategory
		'''
		for pipeline in self.pipelines:
			res = pipeline.retrival(content, adc_cache)
			if res:
				return res
		return []


class CategoryRetrivalStrategyPipeline(object):

	'''
    Abstract class, represent all strategy for recommend
    '''    

	__metaclass__ = ABCMeta

	def __init__(self, builder, distance, ad_c_vec_getter, content_vec_getter, **args):
		pass

	@abstractmethod
	def retrival(self, content, adc_cache):
		'''Find the best ad categorys

		Args:
			content : the content.Content object
			adc_cache : the ad_cache.AdCategoryCache object

		Returns:
			list of best ad categorys(ad.AdCategory)
		'''
		pass


class DefaultCategoryRetrivalStrategyPipeline(CategoryRetrivalStrategyPipeline):

	'''Content category compute cosine with ad category
	'''

	def __init__(self, builder, distance, ad_c_vec_getter, content_vec_getter, **args):
		self.builder = builder
		self.distance = distance
		self.ad_c_vec_getter = ad_c_vec_getter
		self.content_vec_getter = content_vec_getter

	def retrival(self, content, adc_cache):
		content_vec = self.builder.get_vec(self.content_vec_getter(content))
		res = []
		for ad_c in adc_cache:
			ad_c_vec = self.builder.get_vec(self.ad_c_vec_getter(ad_c))
			if self.distance.distance(ad_c_vec, content_vec) > 0:
				res.append(ad_c)
		return res


if __name__ == '__main__':
	center = CategoryRetrivalStrategyCenter()