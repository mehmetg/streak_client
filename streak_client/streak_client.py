import json
import requests
from pipeline import Pipeline
debug = 0
#
#
class StreakClient(object):
	'''Specified basics for the Streak API Client
	Attr:
		api_protocol		protocol to use
		api_base_uri 		api base uri
		api_version			api version
		api_auth 			http auth tuple with api key to be used by the client (instance only)
		api_uri 			complete api uri (instance only)
		pipeline_root_uri	uri to the pipelines root.
		pipelines			list of pipeline objects for the user
							pipeline is a shallow object has only names for members
		whoami				user information
		req 				last http request performed (debug/devel purposes)
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
		self.api_auth = (my_api_key, '')
		#consolidate attributes and build the URI
		all_attributes = self.__class__.__dict__.copy()
		all_attributes.update(self.__dict__)

		self.api_uri = "%(api_protocol)s://%(api_base_uri)s/%(api_version)s" \
						% all_attributes

		self.pipeline_root_uri = self.api_uri + "/pipelines"
		self.pipelines = []
		
		if debug:
			print(self.api_uri)

	def get_pipelines(self):
		'''Gets a list of all pipeline objects. Performs a single GET.
		To go deeper individual pipelines need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			returns 	status code for the GET request.
		'''
		self.req = requests.get(self.pipeline_root_uri, auth = self.api_auth)
		if self.req.status_code == requests.codes.ok:
			pipelines = r.json()
			self.pipelines = []
			for pipeline in pipelines:
				self.pipelines.append(Pipeline(self.api_uri, self.api_auth, pipeline))
		else:
			pass

		return self.req.status_code

	def get_whoami(self):
		'''Get whoami information from the server and update the attribute
		Args:
			return		status code for the get request
		''' 	
		my_uri = self.api_uri + "/users/me"

		self.req = requests.get(my_uri, auth=self.api_auth)
		if(self.req.status_code == requests.codes.ok):
			self.whoami = self.req.json()
		else:
			print("Failed with code: {}".format(r.status_code))
			self.whoami = None
		
		return self.req.status_code

############
############
def main():
	"""Code to run simple demo commands"""
	key = ''
	with open('../STREAK_API_KEY.txt','r') as f:
		key = f.read().strip()

	s_client = StreakClient(key)
	#print(s_client.whoami())
	print('--------')
	s_client.get_pipelines()
	print(s_client.pipelines)


if __name__ == '__main__':
	main()