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
			if op == 'delete':
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

		self.pipeline_root_uri = self.api_uri + '/' + self.pipelines_suffix
		self.box_root_uri = self.api_uri + '/' + self.boxes_suffix
		self.search_uri = self.api_uri + '/' + self.search_suffix
		self.snippet_root_uri = self.api_uri + '/' + self.snippets_suffix

		if DEBUG:
			print(self.api_uri)

	###
	#Private Utility Methods
	###
	def _parse_req(self, req):
		if DEBUG:
			if req.status_code != requests.codes.ok:
				print("code: {}".format(req.status_code))
				print("response {}".format(req.json()))
				print("req headers {}".format(req.request.headers))
				print("req body {}".format(req.request.body))
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

		uri = '/'.join([
						self.api_uri,
						self.pipelines_suffix,
						])
		if sort_by:
			uri += self.sort_by_postfix + sort_by

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
			return self._req('delete', uri)
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
			uri = self.box_root_uri + '/' + self.sort_by_postfix + sort_by
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

		uri = self.pipeline_root_uri + '/' + pipeline_key + '/' + self.boxes_suffix
		
		if sort_by:
			uri +=  '/' + self.sort_by_postfix + sort_by
		
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
		'''Creates a pipeline with the provided attributes.
		Args:
			name	required name string
			kwargs	{name, description, orgWide, aclEntries}
			return	(status code, box dict)
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

		return code, data
	###
	#Snippet Methods
	###
	def get_snippets(self):
		'''Gets all snippets available.
		Args:
			return		(status code, snippets as list(dicts))
		'''
		code, data =   self._req('get', self.snippet_root_uri)
		
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
		
		return code, data
	###
	#Stage Methods
	###
	def get_pipeline_stages(self, pipeline_key):
		'''Gets a list of all stage objects. Performs a single GET.
		To go deeper individual boxes need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			pipeline_key	key for pipeline
			sort_by			in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
			returns 		(status code for the GET request, dict of stages) 
		'''
		if not pipeline_key:
			return requests.codes.bad_request, None

		uri = self.pipeline_root_uri + '/' + pipeline_key + '/' + self.stages_suffix
		
		code, data = self._req('get', uri)

		return code, data.values()
		
	def get_pipeline_stage(self, pipeline_key, stage_key, sort_by = None):
		'''Gets a list of all stage objects. Performs a single GET.
		To go deeper individual boxes need to be polled for their contents.
		This is a directory for what we could ask for.
		Args:
			pipeline_key	key for pipeline
			stage_key		key for stage
			sort_by			in desc order by 'creationTimestamp' or 'lastUpdatedTimestamp'
			returns 		(status code for the GET request, dict of stages) 
		'''
		if not (pipeline_key and stage_key):
			return requests.codes.bad_request, None

		uri = self.pipeline_root_uri + '/' + pipeline_key + '/' + self.stages_suffix + '/' + stage_key
		
		code, data = self._req('get', uri)

		return code, data

	def create_pipeline_stage(self, pipeline_key, name, **kwargs):
		'''Creates a pipeline with the provided attributes.
		Args:
			name	required name string
			kwargs	{name, description, orgWide, aclEntries}
			return	(status code, stage dict)
		'''
		#req sanity check
		if not (pipeline_key and name):
			return requests.codes.bad_request, None

		uri = self.pipeline_root_uri + '/' + pipeline_key + '/' + self.stages_suffix
		kwargs.update({'name':name})

		new_box = StreakStage(**kwargs)
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
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

		uri = self.pipeline_root_uri + '/' + pipeline_key + '/' + self.stages_suffix + '/' +stage_key
		
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
	#Newsfeed Methods
	###
	def _create_field(self, uri , name, field_type, **kwargs):
		'''Creates a pipeline with the provided attributes.
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
			kwargs			{name, type}
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
			uri = '/'.join([uri, field.attributes['key']])
		except KeyError:
			return requests.codes.bad_request, None
	
		code, data = self._req('post', uri , json.dumps(payload))
		
		return code, data

	def get_pipeline_field(self, pipeline_key, field_key = None):
		uri = '/'.join([self.api_uri, 
						self.pipelines_suffix, 
						pipeline_key, 
						self.fields_suffix
						])
		if field_key:
			uri = '/'.join([uri, field_key])

		return self._req('get', uri)

	def create_pipeline_field(self, pipeline_key, name, field_type, **kwargs):
		'''Creates a pipeline with the provided attributes.
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
		uri = '/'.join([self.api_uri,
						self.pipelines_suffix,
						pipeline_key,
						self.fields_suffix
						])
		return self._update_field(uri, field)

	def delete_pipeline_field(self, pipeline_key, field_key):
		uri = '/'.join([self.api_uri,
						self.pipelines_suffix, 
						pipeline_key, 
						self.fields_suffix, 
						field_key
						])
		return self._req('delete', uri)

	def create_box_field(self, box_key, name, field_type, **kwargs):
		raise Exception("Not supported exception!")
		'''Creates a pipeline with the provided attributes.
		Args:
			box_key 		specifying the box to add the field to
			name			required name string
			field_type		required type string [TEXT_INPUT, DATE or PERSON]
			kwargs			{}
			return			(status code, field dict)
		'''
		uri = '/'.join([self.api_uri,
						self.boxes_suffix, 
						box_key,
						self.fields_suffix
						])
		
		code, data = self._create_field(uri, name, field_type, **kwargs)
		
		return code, data

	def update_box_field(self, box_key, field):
		uri = '/'.join([self.api_uri,
						self.boxes_suffix,
						box_key,
						self.fields_suffix
						])
		return self._update_field(uri, field)

	def get_box_field(self, box_key, field_key = None):
		uri = '/'.join([self.api_uri,
						self.boxes_suffix,
						box_key,
						self.fields_suffix
						])
		if field_key:
			uri = '/'.join([uri, field_key])

		return self._req('get', uri)
	
	def delete_box_field(self, box_key, field_key):
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
		if detail_level:
			if detail_level not in ['ALL', 'CONDENSED']:
				return requests.codes.bad_request, {'success' : 'False', 
												'error': 'detailLevel needs to be provided and field_type needs to be \'ALL\' or \'CONDENSED\''}
			uri +=  self.detail_level_suffix + detail_level
		return self._req('get', uri)

	def get_pipeline_newsfeeds(self, pipeline_key, detail_level = None):
		uri = '/'.join([self.api_uri,
						self.pipelines_suffix,
						pipeline_key,
						self.newsfeed_suffix
						])
		return self._get_newsfeeds(uri, detail_level)

	def get_box_newsfeeds(self, box_key, detail_level = None):
		uri = '/'.join([self.api_uri,
						self.boxes_suffix,
						box_key,
						self.newsfeed_suffix
						])
		return self._get_newsfeeds(uri, detail_level)
	###
	#Thread Methods
	###
	def get_thread(self, thread_key):
		uri = '/'.join([self.api_uri,
						self.threads_suffix,
						thread_key
						])
		return self._req('get', uri)

	def get_box_threads(self, box_key):
		uri = '/'.join([self.api_uri,
						self.boxes_suffix,
						box_key,
						self.threads_suffix
						])
		return self._req('get', uri)
	###
	#Comment Methods
	###
	def create_box_comments(self, box_key, message, **kwargs):
		'''Creates a pipeline with the provided attributes.
		Args:
			box_key			key for box
			message			message string
			kwargs			{}
			return			(status code, comment dict)
		'''
		uri = '/'.join([self.api_uri,
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
		uri = '/'.join([self.api_uri,
						self.boxes_suffix,
						box_key,
						self.comments_suffix
						])
		return self._req('get', uri)
	
	def delete_box_comment(self, box_key, comment_key):
		raise Exception("Not supported yet! Or not documented!")
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
			box_key 		specifying the box to add the field to
			message			message for the reminder
			remind_date		date to remind on in ticks.
			remind_follwers true/false
			kwargs			{}
			return			(status code, reminder dict)
		'''
		uri = '/'.join([self.api_uri,
						self.boxes_suffix, 
						box_key,
						self.reminders_suffix
						])
		kwargs.update({	'message':message, 
						'remindDate':remind_date, 
						'remindFollowers': remind_follwers})

		new_rem = StreakReminder(**kwargs)
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
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
	
		#print(new_pl.attributes)
		#print(new_pl.to_dict())
		#raw_input()
		try:
			uri = '/'.join([uri, reminder.attributes['key']])
		except KeyError:
			return requests.codes.bad_request, None
	
		code, data = self._req('post', uri , json.dumps(payload))
		
		return code, data

	def get_box_reminders(self, box_key):
		uri = '/'.join([self.api_uri,
						self.boxes_suffix, 
						box_key,
						self.reminders_suffix
						])

		return self._req('get', uri)

	def get_reminder(self, reminder_key):
		uri = '/'.join([self.api_uri,
						self.reminders_suffix,
						reminder_key
						])
		return self._req('get', uri)

	def delete_reminder(self, reminder_key):
		uri = '/'.join([self.api_uri,
						self.reminders_suffix,
						reminder_key
						])
		return self._req('delete', uri)
	###
	#File Methods
	###
	def get_file(self, file_key):
		uri = '/'.join([self.api_uri,
						self.files_suffix,
						file_key
						])
		return self._req('get', uri)
	
	def get_file_contents(self, file_key):
		uri = '/'.join([self.api_uri,
						self.files_suffix,
						file_key,
						self.file_contents_suffix,
						])
		return self._req('get', uri)
	
	def get_file_link(self, file_key):
		uri = '/'.join([self.api_uri,
						self.files_suffix,
						file_key,
						self.file_link_suffix,
						])
		return self._req('get', uri)

	def get_box_files(self, box_key):
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
	"""Code to run simple demo commands"""
	key = ''
	with open('/Volumes/Users/mehmetgerceker/Desktop/bts/STREAK_API_KEY.txt','r') as f:
		key = f.read().strip()
	
	s_client = StreakClient(key)
	print('key', key)
	box_reminder_api_test(s_client)
	

if __name__ == '__main__':
	main()