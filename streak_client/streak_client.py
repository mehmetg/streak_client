import json, requests
from streak_objects import *

import requests
DEBUG = 1

class StreakClientBaseObject(object):
	'''Specified basics for the Streak API Client
	Attr:
		api_protocol		protocol to use
		api_base_uri 		api base uri
		api_version			api version
		api_auth 			http auth tuple with api key to be used by the client
		api_uri 			complete api uri
	'''

	def __init__(self, my_api_key, **kwargs):
		self.api_protocol = 'https'
		self.api_base_uri = 'www.streak.com/api'
		self.api_version = 'v1'
		#consolidate attributes and build the URI
						
		self.api_uri = "%(api_protocol)s://%(api_base_uri)s/%(api_version)s" \
						% self.__dict__

		self.api_auth = (my_api_key, '')

	def _parse_init_args(self, **kwargs):
		#print("args", kwargs)
		#print("attr:", self.attributes)
		self.attributes.update(kwargs)
	def _get_req_fp(self, op):
		if(op):
			op = op.lower()
			if op == 'get':
				return requests.get, None
			if op == 'put':
				return requests.put, {'Content-Type': 'application/x-www-form-urlencoded'}
			if op == 'post':
				return requests.post, None
			if op == 'del':
				return requests.delete, None
		else:
			raise NotImplementedError('Operation {} is not supported!'.format(op))

	def _req(self, op, uri, payload = None):
		if DEBUG:
			print('uri', uri)

		req_fp, content_type = self._get_req_fp(op)

		if payload:
			if content_type:
				r = req_fp(uri, payload, auth = self.api_auth, headers = content_type)
			else:
				r = req_fp(uri, payload, auth = self.api_auth)
		else:
			r = req_fp(uri, auth = self.api_auth)

		if r.status_code == requests.codes.ok:
			data = r.json()
		else:
			data = None
			pass
		#keep for debugging 

		if DEBUG:
			self.req = r
			print(payload)
			print(uri)
			#print(self.req.)
		return r.status_code, data
	def _form_encode(self, **kwargs):
		out_string = '&'.join(str(k) + '=' + str(v) for k,v in kwargs.iteritems() if v is not None)
		return out_string
#
#
class StreakClient(StreakClientBaseObject):
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
		self.sort_by_postfix = '?sortBy='

		
		if DEBUG:
			print(self.api_uri)

	def get_pipelines(self, sort_by = None):
		'''Gets a list of all pipeline objects. Performs a single GET.
		To go deeper individual pipelines need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			sort_by		in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
			returns 	(status code for the GET request, dict of pipelines)
		'''
		if sort_by:
			uri = self.pipeline_root_uri + self.sort_by_postfix + sort_by
		else:
			uri = self.pipeline_root_uri

		return self._req('get', uri)

	def create_pipeline(self, name, description, **kwargs):
		'''Creates a pipeline with the provided attributes.
		Args:
			name	required name string
			kwargs	{name, description, orgWide, aclEntries}
			return	(status code, pipeline_dict)
		'''
		kwargs.update({'name':name, 'description':description})

		new_pl = StreakPipeline(**kwargs)
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		code, r_data = self._req('put', self.pipeline_root_uri, new_pl.to_dict())
		
		if DEBUG:
			if code != 200:
				print("code: {}".format(code))
				print("response {}".format(self.req.json()))
			

		return code, r_data

	def get_boxes(self, sort_by = None):
		'''Gets a list of all pipeline objects. Performs a single GET.
		To go deeper individual boxes need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			sort_by		in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
			returns 	(status code for the GET request, dict of boxes) 
		'''
		if sort_by:
			uri = self.box_root_uri + self.sort_by_postfix + sort_by
		else:
			uri = self.box_root_uri

		return self._req('get', uri)

	def get_user(self, key = None):
		'''Get user information from the server and update the attribute
		Args:
			key			user key (default: me)
			return		(status code for the get request, dict user data)
		''' 	
		if key:
			uri = self.api_uri + "/users/" + key
		else:
			uri = self.api_uri + "/users/me"

		return self._req('get', uri)

	def search(self, kw):
		'''Takes a keyword and returns the search results.
		Args:
			kw		keyword (str) to search for.
			return	(code, list(dicts))
		'''
		if kw:
			return self._get(self.search_uri + kw)
		else:
			return requests.codes.bad_request, None

	def get_snippets(self):
		'''Gets all snippets available.
		Args:
			return		(status code, snippets as list(dicts))
		'''
		return self._req('get', self.snippet_root_uri)
		
	def get_snippet(self, key):
		'''Get specific snippet by its key
		Args:
			key			snippet key
			return		(status code, snippet dict)
		''' 	
		if kw:
			return self._req('get', self.snippet_root_uri + '/' + key)
		else:
			return requests.codes.bad_request, None
		


############
############
def main():
	"""Code to run simple demo commands"""
	key = ''
	with open('/Volumes/Users/mehmetgerceker/Desktop/bts/STREAK_API_KEY.txt','r') as f:
		key = f.read().strip()
	
	s_client = StreakClient(key)
	#print(s_client.whoami())
	
	
	#print(s_client.get_boxes())
	#print(s_client.get_pipelines())
	code, user_data = s_client.get_user()
	print('---USER---')
	user = StreakUser(**user_data)
	user.show()
	
	print('---Create PIPE---')
	code, data = s_client.create_pipeline("myTest", "myDescription")
	o = StreakPipeline(**data)
	o.show()
	print("---------")
	print('---PIPE---')
	code, data = s_client.get_pipelines()
	for item in data:
		o = StreakPipeline(**item)
		o.show()
		print("---------")

	print("---BOX---")
	code, data = s_client.get_boxes()
	for item in data:
		o = StreakBox(**item)
		o.show()
		print("---------")

if __name__ == '__main__':
	main()