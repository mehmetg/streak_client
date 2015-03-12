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
				return requests.post, {'Content-Type': 'application/json'}
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
		self.search_uri = self.api_uri + "/search?query="
		self.snippet_root_uri = self.api_uri + "/snippets" 
		self.sort_by_postfix = '?sortBy='
		self.boxes_suffix = '/boxes'
		
		if DEBUG:
			print(self.api_uri)

	def _parse_req(self, code):
		if DEBUG:
			if code != 200:
				print("code: {}".format(code))
				print("response {}".format(self.req.json()))
				print("req headers {}".format(self.req.request.headers))
				print("req body {}".format(self.req.request.body))
	###
	#Pipeline Methods
	###
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
	
	def get_pipeline(self, key):
		'''Gets the pipeline with the specified key. Performs a single GET.
		To go deeper individual pipelines need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			returns 	(status code for the GET request, pipeline dict)
		'''
		if key:
			uri = self.pipeline_root_uri + '/' + key
			return self._req('get', uri)
		else:
			return requests.codes.bad_request, None

	def delete_pipeline(self, key):
		'''Deletes the pipeline specified by the key
		Args:
			returns 	(status code for the DELETE request, success message dict)
		'''
		if key:
			uri = self.pipeline_root_uri + '/' + key
			return self._req('del', uri)
		else:
			return requests.codes.bad_request, None

	def create_pipeline(self, name, description, **kwargs):
		'''Creates a pipeline with the provided attributes.
		Args:
			name	required name string
			kwargs	{name, description, orgWide, aclEntries}
			return	(status code, pipeline_dict)
		'''
		#req sanity check
		if not (name and description):
			return requests.codes.bad_request, None

		kwargs.update({'name':name, 'description':description})

		new_pl = StreakPipeline(**kwargs)
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		code, r_data = self._req('put', self.pipeline_root_uri, new_pl.to_dict())
		
		self._parse_req(code)
			
		return code, r_data
	
	def update_pipeline(self, pipeline):
		'''Updates a pipeline with the provided attributes.
		Args:
			key			required identifier for the pipeline
			pipeline	StreakPipeline object
			return		(status code, pipeline_dict)
		'''
		#req sanity check
		payload = None
		if  type(pipeline) is not StreakPipeline:
			return requests.codes.bad_request, None

		payload = pipeline.to_dict(rw = True)
	
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		try:
			uri = self.pipeline_root_uri + '/' + pipeline.attributes['pipelineKey']
		except KeyError:
			return requests.codes.bad_request, None
	
		code, r_data = self._req('post', uri , json.dumps(payload))
		
		#in case there's an error and we're debugging
		self._parse_req(code)
			

		return code, r_data
	###
	#Box Methods
	###
	def get_all_boxes(self, sort_by = None):
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

	def get_box(self, box_key, sort_by = None):
		'''Gets a list of all pipeline objects. Performs a single GET.
		To go deeper individual boxes need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			pipeline_key	key for pipeline
			sort_by			in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
			returns 		(status code for the GET request, dict of boxes) 
		'''
		if not box_key:
			return requests.codes.bad_request, None

		uri = self.box_root_uri + '/' + box_key
		
		return self._req('get', uri)

	def get_pipeline_boxes(self, pipeline_key, sort_by = None):
		'''Gets a list of all pipeline objects. Performs a single GET.
		To go deeper individual boxes need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			pipeline_key	key for pipeline
			sort_by			in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
			returns 		(status code for the GET request, dict of boxes) 
		'''
		if not pipeline_key:
			return requests.codes.bad_request, None

		uri = self.pipeline_root_uri + '/' + pipeline_key + self.boxes_suffix
		
		if sort_by:
			uri += self.sort_by_postfix + sort_by
		
		return self._req('get', uri)

	def delete_box(self, key):
		'''Deletes the box specified by the key
		Args:
			returns 	(status code for the DELETE request, success message dict)
		'''
		if key:
			uri = self.box_root_uri + '/' + key
			return self._req('del', uri)
		else:
			return requests.codes.bad_request, None

	def create_box(self, pipeline_key, name, **kwargs):
		'''Creates a pipeline with the provided attributes.
		Args:
			name	required name string
			kwargs	{name, description, orgWide, aclEntries}
			return	(status code, pipeline_dict)
		'''
		#req sanity check
		if not (pipeline_key and name):
			return requests.codes.bad_request, None

		uri = self.pipeline_root_uri + '/' + pipeline_key + self.boxes_suffix
		kwargs.update({'name':name})

		new_box = StreakBox(**kwargs)
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		code, r_data = self._req('put', uri, new_box.to_dict(rw = True))
		
		#in case there's an error and we're debugging
		self._parse_req(code)
		
			

		return code, r_data
	
	def update_box(self, box):
		'''Updates a box with the provided attributes.
		Args:
			key		required identifier for the box
			kwargs	{name, description, orgWide, aclEntries, ...}
			return	(status code, pipeline_dict)
		'''
		#req sanity check
		payload = None
		if  type(box) is not StreakBox:
			return requests.codes.bad_request, None

		payload = box.to_dict(rw = True)
	
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		try:
			uri = self.box_root_uri + '/' + box.attributes['boxKey']
		except KeyError:
			return requests.codes.bad_request, None
	
		code, r_data = self._req('post', uri , json.dumps(payload))
		
		#in case there's an error and we're debugging
		self._parse_req(code)
			

		return code, r_data
	###
	#User Methods
	###
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
	###
	#Search Methods
	###
	def search(self, kw):
		'''Takes a keyword and returns the search results.
		Works for boxes only?
		Args:
			kw		keyword (str) to search for.
			return	(code, list(dicts))
		'''
		if not kw:
			return requests.codes.bad_request, None

		code, data = self._req('get', self.search_uri + kw)

		self._parse_req(code+1)

		return code, data

	def get_snippets(self):
		'''Gets all snippets available.
		Args:
			return		(status code, snippets as list(dicts))
		'''
		code, data =   self._req('get', self.snippet_root_uri)
		
		self._parse_req(code)

		return code, data

	def get_snippet(self, key):
		'''Get specific snippet by its key
		Args:
			key			snippet key
			return		(status code, snippet dict)
		''' 	
		if not key:
			return requests.codes.bad_request, None

		code, data =  self._req('get', self.snippet_root_uri + '/' + key)
		
		self._parse_req(code)

		return code, data
			
		


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
	'''
	code, user_data = s_client.get_user()
	print('---USER---')
	user = StreakUser(**user_data)
	user.show()
	
	print('---Create PIPE---')
	code, data = s_client.create_pipeline("1", "desc")
	o = StreakPipeline(**data)
	o.show()
	print("---------")
	for i in xrange(5):
		raw_input()
		print('---Update PIPE---')
		o.attributes['name'] = str(int(o.attributes['name']) + 1)
		code, data = s_client.update_pipeline(o)
		o = StreakPipeline(**data)
		o.show()
		print("---------")
	raw_input()
	print('---Delete PIPE---')
	code, data = s_client.delete_pipeline(o.to_dict()['pipelineKey'])
	print(data)
	print("---------")
	raw_input()
	
	print('---ALL PIPES---')
	code, data = s_client.get_pipelines()
	for item in data:
		o = StreakPipeline(**item)
		o.show()
		print("---------")
	print('---ONE PIPE---')
	code, data = s_client.get_pipeline("agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIC5hAoM")
	o = StreakPipeline(**data)
	o.show()
	print("---------")
	print('---ONE PIPE, ALL BOXES---')
	code, data = s_client.get_pipeline_boxes("agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIC5hAoM")
	for item in data:
		o = StreakBox(**item)
		o.show()
		print("---------")
	print("---ONE BOX---")
	code, data = s_client.get_box('agxzfm1haWxmb29nYWVyLwsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIEQ2FzZRjh1AMM')
	o = StreakBox(**data)
	o.show()
	print("---------")
	print("---ALL BOXES---")
	code, data = s_client.get_all_boxes()
	for item in data:
		o = StreakBox(**item)
		o.show()
		print("---------")
	print("---Create BOX---")
	code, data = s_client.create_box('agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIC5hAoM', "1")
	o = StreakBox(**data)
	o.show()
	for i in xrange(5):
		raw_input()
		print('---Update PIPE---')
		o.attributes['name'] = str(int(o.attributes['name']) + 1)
		code, data = s_client.update_box(o)
		o = StreakBox(**data)
		o.show()
		print("---------")
	print("---Search BOXES---")
	code, data = s_client.search("6")
	for item in data['results']:
		o = StreakBox(**item)
		o.show()
		print("---------")
	raw_input()
	print("---Delete BOX---")
	code, data = s_client.delete_box(o.to_dict()['boxKey'])
	print(data)
	'''
	print("---ALL SNIPPETS---")
	code, data = s_client.get_snippets()
	for item in data:
		o = StreakSnippet(**item)
		o.show()
		print("---------")
	print("---ONE SNIPPET---")
	code, data = s_client.get_snippet("sss")
	if(code == 200):
		o = StreakSnippet(**item)
		o.show()
	print("---------")
	
if __name__ == '__main__':
	main()