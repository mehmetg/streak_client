import requests, json
debug = 1
#
#
class StreakClient(object):
	'''Specified basics for the Streak API Client
	Attr:
		api_protocol	protocol to use
		api_base_uri 	api base uri
		api_version		api version
		api_key 		api key to be used by the client (instance only)
		api_uri 		complete api uri (instance only)
	'''

	api_protocol = 'https'
	api_base_uri = 'www.streak.com/api'
	api_version = 'v1'
	
	def __init__(self, my_api_key):
		'''Initializes an instance of the class with an api key
		Allows multiple instances with distinct keys.
		Args:
			my_api_key	api key for this instance
		'''
		self.api_key = my_api_key
		#consolidate attributes and build the URI
		all_attributes = self.__class__.__dict__.copy()
		all_attributes.update(self.__dict__)

		self.api_uri = "%(api_protocol)s://%(api_key)s@%(api_base_uri)s/%(api_version)s" \
						% all_attributes
		if debug:
			print(self.api_uri)



############
############
def main():
	s_client = StreakClient("myKey")

	"""Code to run simple demo commands"""

if __name__ == '__main__':
	main()