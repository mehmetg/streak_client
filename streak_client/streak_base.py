import requests, json, sys
DEBUG = 1

class StreakBase(object):
	'''Specified basics for the Streak API Client
	Attr:
		api_protocol		protocol to use
		api_base_uri 		api base uri
		api_version			api version
		api_auth 			http auth tuple with api key to be used by the client
		api_uri 			complete api uri
	'''

	def __init__(self, my_api_key):
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
				return requests.get
			if op == 'put':
				return requests.put
			if op == 'post':
				return requests.post
			if op == 'del':
				return requests.delete
		else:
			raise NotImplementedError('Operation {} is not supported!'.format(op))

	def _req(self, op, uri, payload = None):
		
		req_fp = self._get_req_fp(op)

		if payload:
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
		return r.status_code, data