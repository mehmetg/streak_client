debug = 1

class StreakBase(object):

	def __init__(self):
		raise NotImplementedError(self.__class__)

	def create(self):
		raise NotImplementedError(self.__class__)

	def delete(self):
		raise NotImplementedError(self.__class__)

	def _parse_init_args(self, kwargs):
		for key in self.attributes:
			try:
				self.__dict__[key] = kwargs[key]
			except KeyError as ke:
				print("Initialization requires the following keys to have valid values:\n" +\
						', '.join((key for key in self.attributes)))
				print("Key: '{}'' not found!".format(key))
				raise ke
				
		if debug:
			print(self.__dict__)