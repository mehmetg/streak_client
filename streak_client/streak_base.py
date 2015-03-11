import requests, json, sys


class StreakBase(object):

	def __init__(self):
		raise NotImplementedError(self.__class__)

	def create(self):
		raise NotImplementedError(self.__class__)

	def delete(self):
		raise NotImplementedError(self.__class__)


	def _parse_init_args(self, **kwargs):
		#print("args", kwargs)
		#print("attr:", self.attributes)
		for key in kwargs:
			try:
				self.attributes[key] = kwargs[key]
			except KeyError:
				#should never happen now"
				pass