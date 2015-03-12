from streak_base import StreakBase
import requests, json

class Pipeline(StreakBase):
	
	def __init__(self, api_uri, client_auth, pipeline_attributes):
		
		self.root_uri = api_uri + '/pipelines'
		#using a dictionary for easy json conversion and seperation 
		#from internals
		#only lists the ones neede/recommended for creation
		self.attributes = {
			'name' : None,
			'description' : None,
			'orgWide': None,
			'fieldNames': None,
			'fieldTypes': None,
			'stages': None,
			'pipelineKey': None
		}
		#non flat attributes of the pipeline
		self.boxes = []
		self.fields  = []
		#update this using the stage order!
		self.stages = []

		self._parse_init_args(**pipeline_attributes)
		
		print(self.__dict__)
		
		self.uri = self.root_uri + '/' + self.attributes['pipelineKey']
		

		self.api_auth = client_auth

	def __str__(self):
		return str(self.__dict__)
	
	#def __repr__(self):
	#	return str(self)

	def create(self):
		payload = json.dumps(self.attributes)
		self.req = requests.put(self.root_uri, payload, auth = None)
		if(self.req.status_code == requests.codes.ok):
			self.attributes= self.req.json()
		else:
			pass
		return self.req.status_code	

	def update(self):
		payload = json.dumps(self.attributes)
		self.req = requests.post(self.root_uri, payload, auth = None)
		if(self.req.status_code == requests.codes.ok):
			self.attributes= self.req.json()
		else:
			pass
		return self.req.status_code

	def get(self):
		self.req = requests.get(self.root_uri, payload, auth = None)
		if(self.req.status_code == requests.codes.ok):
			self.attributes = self.req.json()
		else:
			pass
		return self.req.status_code

	def delete(self):
		self.req = requests.delete(self.uri, auth = None)
		
		return self.req.status_code

	def get_boxes(self):
		pass

	def get_stages(self):
		pass

	def get_fields(self):
		pass

	def set_stage_order():
		'''Validates and sets stage order
		Does not perform a post to update on server side
		Stages for update as we cannot update individual fields.'''
		pass


