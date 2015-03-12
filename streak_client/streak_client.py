import json
from streak_base import StreakBase
debug = 0
#
#
class StreakClient(StreakBase):
	'''Specified basics for the Streak API Client
	Attr:
		api_protocol		protocol to use
		api_base_uri 		api base uri
		api_version			api version
		api_auth 			http auth tuple with api key to be used by the client (instance only)
		api_uri 			complete api uri (instance only)
		******
		pipeline_root_uri	uri to the pipelines root.
		pipelines			list of pipeline objects for the user
							pipeline is a shallow object has only names for members
		whoami				user information
		req 				last http request performed (debug/devel purposes)
	'''

	
	
	def __init__(self, my_api_key):
		'''Initializes an instance of the class with an api key
		Allows multiple instances with distinct keys.
		Args:
			my_api_key	api key for this instance
		'''
		super(StreakClient, self).__init__(my_api_key)

		self.pipeline_root_uri = self.api_uri + "/pipelines"
		self.box_root_uri = self.api_uri + "/boxes"
		self.search_uri = self.api_uri + "?query="
		self.snippet_root_uri = self.api_uri + "/snippets" 
		
		
		if debug:
			print(self.api_uri)

	def get_pipelines(self):
		'''Gets a list of all pipeline objects. Performs a single GET.
		To go deeper individual pipelines need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			returns 	(status code for the GET request, dict of pipelines)
		'''
		return self._req('get', self.pipeline_root_uri)

	def get_boxes(self):
		'''Gets a list of all pipeline objects. Performs a single GET.
		To go deeper individual boxes need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			returns 	(status code for the GET request, dict of boxes) 
		'''
		return self._req('get', self.box_root_uri)


	def get_user(self, ID=None):
		'''Get user information from the server and update the attribute
		Args:
			ID			user ID (default: me)
			return		(status code for the get request, dict user data)
		''' 	
		if ID:
			t_uri = self.api_uri + "/users/" + ID
		else:
			t_uri = self.api_uri + "/users/me"

		return self._req('get', t_uri)

	def search(self, kw):
		if kw:
			return self._get(self.search_uri + kw)
		else:
			return requests.codes.bad_request, None

	def get_snippets(self):
		return self._req('get', self.snippet_root_uri)
	
	def get_snippet(self, key):
		return self._req('get', self.snippet_root_uri + '/' + key)


############
############
def main():
	"""Code to run simple demo commands"""
	key = ''
	with open('/Volumes/Users/mehmetgerceker/Desktop/bts/STREAK_API_KEY.txt','r') as f:
		key = f.read().strip()
	
	sb = StreakBase('aa')

	s_client = StreakClient(key)
	#print(s_client.whoami())
	print('--------')
	
	print(s_client.get_boxes())


if __name__ == '__main__':
	main()