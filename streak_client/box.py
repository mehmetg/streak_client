from streak_base import StreakBase
import requests, json

class Box(StreakBase):


	def __init__(self, api_uri, **kwargs):

		self.attributes = {
				'name': None,
				'notes': None,
				'stageKey': None,
				'fields': None,
				'followerKeys': None,
				'boxKey':  None
		}
		self._parse_init_args(**kwargs)
		#this needs to happen here for the _parse_init_args to work properly.
		self.api_uri = api_uri

	def __str__(self):
		return str(self.__dict__)


	def create(self):
		print(json.dumps(self.attributes))



#########
#########
def main():
	b = Box("h", name  = "alli", followerKeys = ['alie', 'eblia'], notes = 'ss', stageKey = 'a',\
				fields = ['a', 'b'], boxKey  = 'aed' )
	print(b)
if __name__ == '__main__':
	main()