import json, requests
from streak_objects import *

import requests
DEBUG = 0

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
		#updates a dict with the keyword args
		self.attributes.update(kwargs)
	
	def _get_req_fp(self, op):
		'''Decisions on what verb to use and content headers happen here
		Args:
			op 			a string specifying a http verb'''
		if(op):
			op = op.lower()
			if op == 'get':
				return requests.get, None
			if op == 'put':
				return requests.put, {'Content-Type': 'application/x-www-form-urlencoded'}
			if op == 'post':
				return requests.post, {'Content-Type': 'application/json'}
			if op == 'delete':
				return requests.delete, None
		else:
			raise NotImplementedError('Operation {} is not supported!'.format(op))
	
	def _req(self, op, uri, payload = None):
		'''HTTP  reequest wrapper with data packaging fucntionality
		Args:
			op 			http verb in str
			uri 		address of the request
			payload		data to be sent in dict format (default: None) 
						If not provided no data is sent
			return 		code and req response dict (single or list)'''
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

		#in case there's an error and we're debugging
		self._parse_req(r)

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
		sort_by_postfix		'?sortBy=' uri building block
		boxes_suffix		'boxes' uri building block
		stages_suffix		'stages' uri building block
		pipelines_suffix	'pipelines' uri building block
		search_suffix		'search?query=' uri building block
		snippets_suffix		'snippets' uri building block
		fields_suffix		'fields' uri building block
		newsfeed_suffix		'newsfeed' uri building block
		threads_suffix		'threads' uri building block
		comments_suffix		'comments' uri building block
		files_suffix		'files' uri building block
		file_contents_suffix'contents' uri building block
		file_link_suffix	'link' uri building block
		reminders_suffix	'reminders' uri building block
		detail_level_suffix	'?detailLevel=' uri building block
	'''
	def __init__(self, my_api_key):
		'''Initializes an instance of the class with an api key
		Allows multiple instances with distinct keys.
		Args:
			my_api_key	api key for this instance
		'''
		super(self.__class__, self).__init__(my_api_key)

		self.sort_by_postfix = '?sortBy='
		self.boxes_suffix = 'boxes'
		self.stages_suffix = 'stages'
		self.pipelines_suffix = 'pipelines'
		self.search_suffix = 'search?query='
		self.snippets_suffix = 'snippets'
		self.fields_suffix = 'fields'
		self.newsfeed_suffix = 'newsfeed'
		self.threads_suffix = 'threads'
		self.comments_suffix = 'comments'
		self.files_suffix = 'files'
		self.file_contents_suffix = 'contents'
		self.file_link_suffix = 'link'
		self.reminders_suffix = 'reminders'
		self.detail_level_suffix = '?detailLevel='

		if DEBUG:
			print(self.api_uri)

	###
	#Private Utility Methods
	###
	def _parse_req(self, req):
		'''Parses a request object for relevant debugging information. Only works
		if DEBUG is enabled.
		Args:
			req 			requests req object
		'''
		if DEBUG:
			if req.status_code != requests.codes.ok:
				print("code: {}".format(req.status_code))
				print("response {}".format(req.json()))
				print("req headers {}".format(req.request.headers))
				print("req body {}".format(req.request.body))

	def _raise_unimplemented_error(self):
		'''Exception helper for raising exceptions for unimplemented class members'''
		import inspect 
		raise NotImplementedError("{} is not implemented yet!".format(inspect.stack()[0][3]))
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
	#Pipeline Methods
	###
	def get_pipeline(self, pipeline_key = None, sort_by = None):
		'''Gets a list of one/all pipeline objects. Performs a single GET.
		To go deeper individual pipelines need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			pipeline_key	specifies pipeline to get. (default = None i.e. ALL)
			sort_by			in desc order by 'creationTimestamp' or 
							'lastUpdatedTimestamp' (ignored when a pipeline_key
							is supplied)
			returns 		(status code for the GET request, dict of pipelines)
		'''
		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						])
		if pipeline_key:
			uri = '/'.join([
							uri,
							pipeline_key
							])
		else:
			if sort_by:
				if sort_by in ['creationTimestamp', 'lastUpdatedTimestamp']:
					uri += self.sort_by_postfix + sort_by
				else:		
					return requests.codes.bad_request, {'success' : 'False', 
												'error': 'sortBy needs to be \'creationTimestamp\', or \'lastUpdatedTimestamp\''}


		return self._req('get', uri)

	def delete_pipeline(self, pipeline_key):
		'''Deletes the pipeline specified by the key
		Args:
			returns 	(status code for the DELETE request, success message dict)
						expect (200 , {'success': 'true'}) for successful execution}
		'''
		if pipeline_key:
			uri = '/'.join([
							self.api_uri,
							self.pipelines_suffix,
							pipeline_key
							])
			return self._req('delete', uri)
		else:
			return requests.codes.bad_request, None
	
	def delete_all_pipelines(self):
		'''Deletes all pipelines
		Args:
			returns		OK for overall success or last error code, resp data.
		'''
		code, data = self.get_pipeline()
		if code == requests.codes.ok:
			for pl_data in data:
				c, d = self.delete_pipeline(pl_data['pipelineKey'])
				if c != requests.codes.ok:
					code = c
					data = d
		return code, data		

	def create_pipeline(self, name, description, **kwargs):
		'''Creates a pipeline with the provided attributes.
		Args:
			name	required name string
			kwargs	{name, description, orgWide, aclEntries} user 
			specifiable ones only
			return	(status code, pipeline_dict) (as created)
		'''
		#req sanity check
		if not (name and description):
			return requests.codes.bad_request, None

		kwargs.update({'name':name, 'description':description})

		new_pl = StreakPipeline(**kwargs)
		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix
						])
		code, r_data = self._req('put', uri, new_pl.to_dict())
		
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

		try:
			uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						pipeline.attributes['pipelineKey']
						])
		except KeyError:
			return requests.codes.bad_request, None
	
		code, r_data = self._req('post', uri , json.dumps(payload))

		return code, r_data
	###
	#Box Methods
	###
	def get_box(self, box_key = None, sort_by = None):
		'''Gets a list of one/all box objects. Performs a single GET.
		To go deeper individual boxes need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			box_key		key for the target box (default: None i.e. ALL)
			sort_by		in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
			returns 	(status code for the GET request, dict of box or a list thereof) 
		'''
		uri = '/'.join([
						self.api_uri,
						self.boxes_suffix
						])
		if box_key:
			uri = '/'.join([
							uri,
							box_key
							])
		if sort_by:
				if sort_by in ['creationTimestamp', 'lastUpdatedTimestamp']:
					uri += self.sort_by_postfix + sort_by
				else:		
					return requests.codes.bad_request, {'success' : 'False', 
												'error': 'sortBy needs to be \'creationTimestamp\', or \'lastUpdatedTimestamp\''}
		return self._req('get', uri)

	def get_pipeline_boxes(self, pipeline_key, sort_by = None):
		'''Gets a list of all box objects in a pipeline. Performs a single GET.
		Args:
			pipeline_key	key for pipeline
			sort_by			in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
							Not sure if it is supported
			returns 		(status code for the GET request, dict of boxes) 
		'''
		if not pipeline_key:
			return requests.codes.bad_request, None

		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						pipeline_key
						])
		
		if sort_by:
				if sort_by in ['creationTimestamp', 'lastUpdatedTimestamp']:
					uri += self.sort_by_postfix + sort_by
				else:		
					return requests.codes.bad_request, {'success' : 'False', 
												'error': 'sortBy needs to be \'creationTimestamp\', or \'lastUpdatedTimestamp\''}
		
		return self._req('get', uri)

	def delete_box(self, key):
		'''Deletes the box specified by the key
		Args:
			returns 	(status code for the DELETE request, success message dict)
		'''
		if key:
			uri = self.box_root_uri + '/' + key
			return self._req('delete', uri)
		else:
			return requests.codes.bad_request, None

	def create_pipeline_box(self, pipeline_key, name, **kwargs):
		'''Creates a box int the pipeline specified with the provided attributes.
		Args:
			name	required name string
			kwargs	{...} see StreakBox object for details
			return	(status code, box dict)
		'''
		#req sanity check
		if not (pipeline_key and name):
			return requests.codes.bad_request, None

		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						pipeline_key,
						self.boxes_suffix
						]) 

		kwargs.update({'name':name})

		new_box = StreakBox(**kwargs)
		
		code, data = self._req('put', uri, new_box.to_dict(rw = True))
		
		return code, data
	
	def update_box(self, box):
		'''Updates a box with the provided attributes.
		Args:
			box 	StreakBox object with updated info
			return	(status code, box in dict form)
		'''
		#req sanity check
		payload = None
		if  type(box) is not StreakBox:
			return requests.codes.bad_request, None

		payload = box.to_dict(rw = True)

		try:
			uri = self.box_root_uri + '/' + box.attributes['boxKey']
		except KeyError:
			return requests.codes.bad_request, None
	
		code, data = self._req('post', uri , json.dumps(payload))

		return code, data
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

		return code, data
	###
	#Snippet Methods
	###
	def get_snippet(self, snippet_key = None):
		'''Get all/one specific snippet by its key
		Args:
			key			snippet key (default: None i.e. ALL)
			return		(status code, snippet dict or list thereof)
		'''
		uri = '/'.join([
						self.api_uri,
						self.snippets_suffix
						])
		if snippet_key:
			uri = '/'.join([
							uri,
							snippet_key
							])

		code, data =  self._req('get', uri)
		
		return code, data
	###
	#Stage Methods
	###
	def get_pipeline_stage(self, pipeline_key, stage_key = None, sort_by = None):
		'''Gets a list of one/all stage objects in a pipeline. Performs a single GET.
		Args:
			pipeline_key	key for pipeline
			stage_key 		key for stage (default: None i.e. ALL)
			sort_by			in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
							may or may not be supported
			returns 		(status code for the GET request, dict of stages)
							It is not a list hence the .values() before return
		'''
		if not pipeline_key:
			return requests.codes.bad_request, None

		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						pipeline_key,
						self.stages_suffix
						])
		if stage_key:
			uri = '/'.join([
							uri,
							stage_key
							])
		
		if sort_by:
				if sort_by in ['creationTimestamp', 'lastUpdatedTimestamp']:
					uri += self.sort_by_postfix + sort_by
				else:		
					return requests.codes.bad_request, {'success' : 'False', 
												'error': 'sortBy needs to be \'creationTimestamp\', or \'lastUpdatedTimestamp\''}

		code, data = self._req('get', uri)
		
		#format is ambigious so we need to rely on user input
		if stage_key:
			data = data.values()
		
		return code, data
		
	def create_pipeline_stage(self, pipeline_key, name, **kwargs):
		'''Creates a pipeline stage with the provided attributes.
		Args:
			name	required name string
			kwargs	{..} see StreakStage object for details
			return	(status code, stage dict)
		'''
		#req sanity check
		if not (pipeline_key and name):
			return requests.codes.bad_request, None

		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						pipeline_key,
						self.stages_suffix])
		
		kwargs.update({'name':name})

		new_box = StreakStage(**kwargs)
		
		code, data = self._req('put', uri, new_box.to_dict(rw = True))
		
		return code, data
	
	def delete_pipeline_stage(self, pipeline_key, stage_key, sort_by = None):
		'''Deletes a stage in the pipeline by stage key and pipeline key
		Args:
			pipeline_key	key for pipeline
			stage_key		key for stage
			sort_by			in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
			returns 		(status code for the GET request, dict of op report) 
		'''
		if not (pipeline_key and stage_key):
			return requests.codes.bad_request, None

		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						pipeline_key,
						self.stages_suffix,
						stage_key
						])
		
		code, data = self._req('delete', uri)
		
		return code, data

	def update_pipeline_stage(self, stage):
		'''Updates a box with the provided attributes.
		Args:
			pipeline_key	reqiured identifier for the pipeline
			stage			StreakStage object
			kwargs			{name}
			return			(status code, stage dict)
		'''
		#req sanity check
		payload = None
		if  type(stage) is not StreakStage:
			return requests.codes.bad_request, None

		payload = stage.to_dict(rw = True)
	
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		try:
			uri = '/'.join([self.api_uri,
							self.pipelines_suffix,
							stage.attributes['pipelineKey'],
							self.stages_suffix,
							stage.attributes['key']
							])
		except KeyError:
			return requests.codes.bad_request, None
	
		code, data = self._req('post', uri , json.dumps(payload))
		
		return code, data
	###
	#Fields Methods
	###
	def _create_field(self, uri , name, field_type, **kwargs):
		'''Creates a field with the provided attributes.
		Args:
			uri		base uri for the field (pipeline or box uri)
			name	required name string
			field_type	required type string [TEXT_INPUT, DATE or PERSON]
			kwargs	{}
			return	(status code, field dict)
		'''
		#req sanity check
		if not (name and (field_type in ['TEXT_INPUT', 'DATE', 'PERSON'])):
			return requests.codes.bad_request, {'success' : 'False', 
												'error': 'name needs to be provided and field_type needs to be \'TEXT_INPUT\', \'DATE\' or \'PERSON\''}

		kwargs.update({'name':name, 'type':field_type})

		new_box = StreakField(**kwargs)
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		code, data = self._req('put', uri, new_box.to_dict(rw = True))
		
		return code, data

	def _update_field(self, uri, field):
		'''Updates a field with the provided attributes.
		Args:
			key	reqiured identifier for the pipeline or box
			field			StreakField object
			kwargs			{name, type} see StreakField for details
			return			(status code, field dict)
		'''
		#req sanity check
		payload = None
		if  type(field) is not StreakField:
			return requests.codes.bad_request, None

		payload = field.to_dict(rw = True)
	
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		try:
			uri = '/'.join([
							uri, 
							field.attributes['key']
							])
		except KeyError:
			return requests.codes.bad_request, None
	
		code, data = self._req('post', uri , json.dumps(payload))
		
		return code, data

	def get_pipeline_field(self, pipeline_key, field_key = None):
		'''Gets one/all field in a pipeline
		Args:
			pipeline_key 		key for pipeline
			field_key 			key for field (default: None i.e. ALL)
			returns				status code, field dict or list thereof
		'''
		uri = '/'.join([
						self.api_uri, 
						self.pipelines_suffix, 
						pipeline_key, 
						self.fields_suffix
						])
		if field_key:
			uri = '/'.join([uri, field_key])

		return self._req('get', uri)

	def create_pipeline_field(self, pipeline_key, name, field_type, **kwargs):
		'''Creates a pipeline field with the provided attributes.
		Args:
			pipeline_key	specifying the pipeline to add the field to
			name			required name string
			field_type		required type string [TEXT_INPUT, DATE or PERSON]
			kwargs			{}
			return			(status code, field dict)
		'''

		uri = '/'.join([self.api_uri,
						self.pipelines_suffix,
						pipeline_key,
						self.fields_suffix
						])
		
		code, data = self._create_field(uri, name, field_type, **kwargs)
		
		return code, data

	def update_pipeline_field(self, pipeline_key, field):
		'''Upates pipeline field as specified
		Args:
			pipeline_key		key for pipeline where the fields lives
			field 				StreakField object with fresh data
			returns				(status code, updated field dict)
		'''
		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						pipeline_key,
						self.fields_suffix
						])
		return self._update_field(uri, field)

	def delete_pipeline_field(self, pipeline_key, field_key):
		'''Deletes pipeline field as specified by key(s)
		Args:
			pipeline_key		key for pipeline where the fields lives
			field_key			field to be deleted
			returns				(status code, resp data)
		'''
		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix, 
						pipeline_key, 
						self.fields_suffix, 
						field_key
						])

		return self._req('delete', uri)

	def get_box_field(self, box_key, field_key = None):
		'''Gets one/all field in a box
		Args:
			box_key 		key for pipeline
			field_key 			key for field (default: None i.e. ALL)
			returns				status code, field dict or list thereof
		'''
		#does not work
		self._raise_unimplemented_error()
		
		uri = '/'.join([self.api_uri,
						self.boxes_suffix,
						box_key,
						self.fields_suffix
						])
		if field_key:
			uri = '/'.join([uri, field_key])

		return self._req('get', uri)

	def create_box_field(self, box_key, name, field_type, **kwargs):
		'''Creates a box field with the provided attributes.
		Args:
			box_key			specifying the box to add the field to
			name			required name string
			field_type		required type string [TEXT_INPUT, DATE or PERSON]
			kwargs			{}
			return			(status code, field dict)
		'''
		#does not work
		self._raise_unimplemented_error()
		
		uri = '/'.join([self.api_uri,
						self.boxes_suffix, 
						box_key,
						self.fields_suffix
						])
		
		code, data = self._create_field(uri, name, field_type, **kwargs)
		
		return code, data

	def update_box_field(self, box_key, field):
		'''Upates box field as specified
		Args:
			box_key		key for pipeline where the fields lives
			field 				StreakField object with fresh data
			returns				(status code, updated field dict)
		'''
		#does not work
		self._raise_unimplemented_error()
		
		uri = '/'.join([self.api_uri,
						self.boxes_suffix,
						box_key,
						self.fields_suffix
						])
		return self._update_field(uri, field)
	
	def delete_box_field(self, box_key, field_key):
		'''Deletes pipeline field as specified by key(s)
		Args:
			pipeline_key		key for pipeline where the fields lives
			field_key			field to be deleted
			returns				(status code, resp data)
		'''
		#does not work
		self._raise_unimplemented_error()

		uri = '/'.join([self.api_uri, 
						self.boxes_suffix, 
						box_key, 
						self.fields_suffix, 
						field_key
						])
		return self._req('delete', uri)
	###
	#Newsfeed Methods
	###
	def _get_newsfeeds(self, uri, detail_level = None):
		'''General purpose function to get newsfeeds
		Args:
			uri 			uri for the feed base
			detail_level 	arguments for req str ['ALL', 'CONDENSED']
			return 			list of feed dicts parse at your convenience
		'''
		if detail_level:
			if detail_level not in ['ALL', 'CONDENSED']:
				return requests.codes.bad_request, {'success' : 'False', 
												'error': 'detailLevel needs to be provided and field_type needs to be \'ALL\' or \'CONDENSED\''}
			uri +=  self.detail_level_suffix + detail_level
		return self._req('get', uri)

	def get_pipeline_newsfeeds(self, pipeline_key, detail_level = None):
		'''Function to get newsfeed for a pipeline
		Args:
			pipeline_key	pipeline key
			detail_level 	arguments for req str ['ALL', 'CONDENSED']
			return 			list of feed dicts parse at your convenience
		'''
		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						pipeline_key,
						self.newsfeed_suffix
						])
		return self._get_newsfeeds(uri, detail_level)

	def get_box_newsfeeds(self, box_key, detail_level = None):
		'''Function to get newsfeed for a pipeline
		Args:
			box 			pipeline key
			detail_level 	arguments for req str ['ALL', 'CONDENSED']
			return 			list of feed dicts parse at your convenience
		'''
		uri = '/'.join([
						self.api_uri,
						self.boxes_suffix,
						box_key,
						self.newsfeed_suffix
						])
		return self._get_newsfeeds(uri, detail_level)
	###
	#Thread Methods
	###
	def get_thread(self, thread_key):
		'''Gets a thread specified by thread_key
		Args:
			thread_key 		thread to get
			returns 		a thread dict
		'''
		uri = '/'.join([self.api_uri,
						self.threads_suffix,
						thread_key
						])
		return self._req('get', uri)

	def get_box_threads(self, box_key):
		'''Gets all threads in a specified box
		Args:
			box_key 		box to look in
			returns 		a list of thread dicts
		'''
		uri = '/'.join([
						self.api_uri,
						self.boxes_suffix,
						box_key,
						self.threads_suffix
						])
		return self._req('get', uri)
	###
	#Comment Methods
	###
	def create_box_comments(self, box_key, message, **kwargs):
		'''Creates a comments in a box with the provided attributes.
		Args:
			box_key			key for box
			message			message string
			kwargs			{} see StreakComment object for more information
			return			(status code, comment dict)
		'''
		uri = '/'.join([
						self.api_uri,
						self.boxes_suffix,
						box_key,
						self.comments_suffix
						])

		if not (box_key and message):
			return requests.codes.bad_request, None

		kwargs.update({'message':message})

		new_cmt = StreakComment(**kwargs)
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		code, r_data = self._req('put', uri, new_cmt.to_dict())
		
		return code, r_data
	
	def get_box_comments(self, box_key):
		'''Gets comments in a box with the provided attributes.
		Args:
			box_key			key for box
			return			(status code, list of comment dicts)
		'''
		uri = '/'.join([
						self.api_uri,
						self.boxes_suffix,
						box_key,
						self.comments_suffix
						])
		return self._req('get', uri)
	
	def delete_box_comment(self, box_key, comment_key):
		'''Deletes comment in a box with the comment_key
		Args:
			box_key			key for box
			return			(status code, list of comment dicts)
		'''
		#does not work
		self._raise_unimplemented_error()

		uri = '/'.join([self.api_uri,
						self.boxes_suffix,
						box_key,
						self.comments_suffix,
						comment_key
						])
		return self._req('delete', uri)
	###
	#Reminder Methods
	###
	def create_box_reminder(self, box_key, message, remind_date, remind_follwers, **kwargs):
		'''Creates a reminder with the provided attributes.
		Args:
			box_key 			specifying the box to add the field to
			message				message for the reminder
			remind_date			date to remind on in ticks.
			remind_followers	true/false
			kwargs				{..} see StreakReminder object for details
			return				(status code, reminder dict)
		'''
		uri = '/'.join([
						self.api_uri,
						self.boxes_suffix, 
						box_key,
						self.reminders_suffix
						])
		kwargs.update({	'message':message, 
						'remindDate':remind_date, 
						'remindFollowers': remind_follwers})

		new_rem = StreakReminder(**kwargs)
		
		code, data = self._req('put', uri, new_rem.to_dict(rw = True))
		
		return code, data	

	def update_reminder(self, reminder):
		'''Creates a reminder with the provided attributes.
		Args:
			reminder		updated reminder of StreakReminder type
			return			(status code, reminder dict)
		'''
		uri = '/'.join([self.api_uri,
						self.reminders_suffix,
						])
		#req sanity check
		payload = None
		if  type(reminder) is not StreakReminder:
			return requests.codes.bad_request, None

		payload = reminder.to_dict(rw = True)
	
		try:
			uri = '/'.join([uri, reminder.attributes['key']])
		except KeyError:
			return requests.codes.bad_request, None
	
		code, data = self._req('post', uri , json.dumps(payload))
		
		return code, data

	def get_box_reminders(self, box_key):
		'''Gets all reminders for a box
		Args:
			reminder		updated reminder of StreakReminder type
			return			(status code, reminder dict)
		'''
		#required sanity check
		if box_key:
			return requests.codes.bad_request, None

		uri = '/'.join([self.api_uri,
						self.boxes_suffix, 
						box_key,
						self.reminders_suffix
						])

		return self._req('get', uri)

	def get_reminder(self, reminder_key):
		'''Gets one reminder
		Args:
			reminder_key	key for the reminder to get
			return			(status code, reminder dict)
		'''
		#required sanity check
		if reminder_key:
			return requests.codes.bad_request, None
		
		uri = '/'.join([
						self.api_uri,
						self.reminders_suffix,
						reminder_key
						])

		return self._req('get', uri)

	def delete_reminder(self, reminder_key):
		'''Deletes specified reminder
		Args:
			reminder_key	key for the reminder to get
			return			(status code, resp key)
		'''
		#required sanity check
		if reminder_key:
			return requests.codes.bad_request, None

		uri = '/'.join([self.api_uri,
						self.reminders_suffix,
						reminder_key
						])
		return self._req('delete', uri)
	###
	#File Methods
	###
	def get_file(self, file_key):
		'''Gets file information
		Args:
			file_key		key for the file to get
			return			(status code, dict of file info)
		'''
		uri = '/'.join([
						self.api_uri,
						self.files_suffix,
						file_key
						])

		return self._req('get', uri)
	
	def get_file_contents(self, file_key):
		'''Gets file contents
		Args:
			file_key		key for the file 
			return			(status code, ?)
		'''
		#does not work
		self._raise_unimplemented_error()
		
		uri = '/'.join([self.api_uri,
						self.files_suffix,
						file_key,
						self.file_contents_suffix,
						])
		return self._req('get', uri)
	
	def get_file_link(self, file_key):
		'''Gets link to file
		Args:
			file_key		key for the file 
			return			(status code, ?)
		'''
		#does not work
		self._raise_unimplemented_error()

		uri = '/'.join([self.api_uri,
						self.files_suffix,
						file_key,
						self.file_link_suffix,
						])
		return self._req('get', uri)

	def get_box_files(self, box_key):
		'''Gets to file infos in a single box.
		Args:
			box_key		key for the file 
			return		(status code, list of file info dicts)
		'''
		uri = '/'.join([self.api_uri,
						self.boxes_suffix,
						box_key,
						self.files_suffix
						])

		return self._req('get', uri)

############
#Main
############
def main():
	#I do nothing but facilitate tests during dev time.
	pass

if __name__ == '__main__':
	main()