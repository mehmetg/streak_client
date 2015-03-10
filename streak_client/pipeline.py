from streak_base import StreakBase
import requests, json
class Pipeline(StreakBase):
	
	def __init__(self, api_uri, pipeline_attributes):
		
		self.uri = api_uri + '/pipelines'
		#using a dictionary for easy json conversion and seperation 
		#from internals
		self.attributes = {
			'name' : None,
			'description' : None,
			'orgWide': None,
			'fieldNames': None,
			'fieldTypes': None,
			'stages': None,
			'pipelineKey': None
		}
		
		self._parse_init_args(attributes)
		

	def create(self):
		print(json.dumps(self.attributes))




