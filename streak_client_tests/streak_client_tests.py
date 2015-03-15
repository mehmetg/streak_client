import unittest

if __name__ == '__main__':
	import sys
	import os
	sys.path.append(os.path.abspath(".."))
	from streak_client import *
	del sys
	del os
elif len(__name__.split('.')) > 2:
	#nose tests compatibility
	from ..streak_client import *
else:
	#py.test
	from streak_client import *

class StreakClientTestBase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		#borrowed from: https://github.com/kredei/streak_client/
		key = '0b6359c686584bc3b610a640e2e7eb9f'
		cls.client = StreakClient(key)
	@classmethod
	def tearDownClass(cls):
		del cls.client

class StreakClientUserAPITest(StreakClientTestBase):
	###
	#Unittest basics
	###
	
	def test_get_user_me(self):
		code, data = self.client.get_user()
		self.assertEqual(code, 200, "Response is not OK. Code: {}".format(code))
	
	def test_get_user_by_key(self):
		code, data = self.client.get_user()
		user_key = data['userKey']
		code, data = self.client.get_user(user_key)
		self.assertEqual(code, 200, "Response is not OK. Code: {}".format(code))
		
	def test_get_user_by_key_invalid_key(self):
		code, data = self.client.get_user(' ')
		self.assertEqual(code, 400, "Response is not '400'. Code: {}".format(code))
		
class StreakClientPipelineAPITest(StreakClientTestBase):
	'''Touches most API related to Pipelines.
	This is not exactly unittesting though.
	'''
	def setUp(self):
		#do nothing unless we want to create stuff here in the future
		pass
	def tearDown(self):
		#delete all pipelines.
		#assumes get_all and delete work fine.
		pass

	def test_create_update_get_delete_one_pipeline(self):
		#create entry
		code, data = self.client.create_pipeline('my_name', 'my_description')
		self.assertEqual(code, 200, "Create response is not OK. Code: {}".format(code))
		self.assertTrue('name' in data and data['name'] == 'my_name', 
						'Create response content is missing!')
		#update entry
		
		pl = StreakPipeline(**data)
		
		pl.attributes['name'] = "new_name"
		pl.attributes['description'] = "new_description"

		#update the pipeline
		code, data = self.client.update_pipeline(pl)
		self.assertEqual(code, 200, "Update response is not OK. Code: {}".format(code))
		new_pl = StreakPipeline(**data)
		
		#check the new values.
		self.assertDictEqual(pl.to_dict(rw=True), new_pl.to_dict(rw=True), "Update data failed!")
		#get entry
		code, data = self.client.get_pipeline(data['pipelineKey'])
		self.assertEqual(code, 200, "Get response is not OK. Code: {}".format(code))
		self.assertTrue('name' in data and data['name'] == 'new_name', 
						'Get response content is missing!')
		#delete entry
		code, data = self.client.delete_pipeline(data['pipelineKey'])
		self.assertEqual(code, 200, "Delete response is not OK. Code: {}".format(code))
	def test_delete_all_pipelines(self):
		code, data = self.client.delete_all_pipelines()
		self.assertEqual(code, 200, "Delete all response not OK. Code: {}".format(code))
		code, data = self.client.get_pipeline()
		self.assertEqual(len(data), 0, "Expected: 0, Read: {}".format(len(data)))
	def test_get_delete_all_pipelines(self):
		num_pl = 10
		for i in xrange(num_pl):
			code, data = self.client.create_pipeline('my_name' + str(i), 'my_description' + str(i))
			self.assertEqual(code, 200, "Create response is not OK. Code: {}".format(code))
			self.assertTrue('name' in data and data['name'] == 'my_name' + str(i), 
							'Create response content is missing!')
		code, data = self.client.get_pipeline()
		self.assertEqual(len(data), num_pl, "Created: {}, Read: {}".format(num_pl, len(data)))

		code, data = self.client.delete_all_pipelines()
		self.assertEqual(code, 200, "Delete all response not OK. Code: {}".format(code))
		code, data = self.client.get_pipeline()
		self.assertEqual(len(data), 0, "Expected: 0, Read: {}".format(len(data)))
'''	
############
#Temporary test routines.
############
def user_api_test(s_client):
	code, user_data = s_client.get_user()
	print('---ME---')
	user = StreakUser(**user_data)
	user.show()
	print('---USER BY ID---')
	code, user_data = s_client.get_user(user.attributes['userKey'])
	user = StreakUser(**user_data)
	user.show()
def pipeline_api_test(s_client):	
	print('---Create PIPELINE---')
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
	print('---Delete PIPELINE---')
	code, data = s_client.delete_pipeline(o.to_dict()['pipelineKey'])
	print(data)
	print("---------")
	raw_input()
	
	print('---GET ALL PIPELINES---')
	code, data = s_client.get_pipelines()
	for item in data:
		o = StreakPipeline(**item)
		o.show()
		print("---------")
	print('---GET ONE PIPELINE---')
	code, data = s_client.get_pipeline("agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIC5hAoM")
	o = StreakPipeline(**data)
	o.show()
	print("---------")
def box_api_test(s_client):
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
		print('---Update BOX---')
		o.attributes['name'] = str(int(o.attributes['name']) + 1)
		code, data = s_client.update_box(o)
		o = StreakBox(**data)
		o.show()
		print("---------")
def search_api_test(s_client):
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
def snippet_api_test(s_client):
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
def stage_api_test(s_client):
	print('---ONE PIPE, ALL STAGES---')
	code, data = s_client.get_pipeline_stages("agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIDyiAoM")
	raw_input()
	for item in data:
		o = StreakStage(**item)
		o.show()
		print("------------------")
	print("---ONE STAGE---")
	code, data = s_client.get_pipeline_stage('agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIDyiAoM', '5001')
	pprint(data)
	o = StreakStage(**data)
	o.show()
	print("------------------")
	print("---Create STAGE---")
	code, data = s_client.create_pipeline_stage('agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIDyiAoM', "1")
	data.update({'pipelineKey':'agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIDyiAoM'})
	o = StreakStage(**data)
	o.show()
	for i in xrange(5):
		raw_input()
		print("---Update STAGE---")
		o.attributes['name'] = str(int(o.attributes['name']) + 1)
		code, data = s_client.update_pipeline_stage(o)
		data.update({'pipelineKey':'agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIDyiAoM'})
		o = StreakStage(**data)
		o.show()
		print("------------------")
	raw_input()
	print("---Delete BOX---")
	code, data = s_client.delete_pipeline_stage(o.attributes['pipelineKey'], o.attributes['key'])
	print(data)
def pipeline_field_api_test(s_client):
	pipeline_key = 'agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIDyiAoM'
	print('---ONE PIPE, CREATE FIELD---')
	code, data = s_client.create_pipeline_field(pipeline_key, 'myField', 'TEXT_INPUT')
	if(code == 200):
		o = StreakField(**data)
		o.show()
	print("------------------")
	raw_input()
	print('---ONE PIPE, CREATE FIELD---')
	code, data = s_client.create_pipeline_field(pipeline_key, 'myField2', 'PERSON')
	if(code == 200):
		o = StreakField(**data)
		o.show()
	print("------------------")
	raw_input()
	print('---ONE PIPE, ALL FIELDS---')
	code, data = s_client.get_pipeline_field(pipeline_key)
	if(code == 200):
		for item in data:
			o = StreakField(**item)
			o.show()
			print("------------------")
	raw_input()
	print("---ONE FIELD---")
	code, data = s_client.get_pipeline_field(pipeline_key, o.attributes['key'])
	if(code == 200):
		o = StreakField(**data)
		o.show()
	print("------------------")
	raw_input()
	print("---UPDATE FIELD---")
	for i in xrange(5):
		o.attributes['name'] += str(i)
		code, data = s_client.update_pipeline_field(pipeline_key, o)
		if(code == 200):
			o = StreakField(**data)
			o.show()
		print("------------------")
	raw_input()
	print('---ONE PIPE, DELETE ALL FIELDS---')
	code, data = s_client.get_pipeline_field(pipeline_key)
	if(code == 200):
		for item in data:
			o = StreakField(**item)
			o.attributes['pipelineKey'] = pipeline_key
			o.show()
			print("---Delete FIELD---")
			code, data = s_client.delete_pipeline_field(o.attributes['pipelineKey'], o.attributes['key'])
			pprint(data)
			print("------------------")
	raw_input()
def box_field_api_test(s_client):
	box_key ='agxzfm1haWxmb29nYWVyLwsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIEQ2FzZRjhxQgM'
	print('---ONE BOX, CREATE FIELD---')
	code, data = s_client.create_box_field(box_key, 'myField', 'TEXT_INPUT')
	if(code == 200):
		o = StreakField(**data)
		o.show()
	print("------------------")
	raw_input()
	print('---ONE BOX, CREATE FIELD---')
	code, data = s_client.create_box_field(box_key, 'myField2', 'PERSON')
	if(code == 200):
		o = StreakField(**data)
		o.show()
	print("------------------")
	raw_input()
	print('---ONE BOX, ALL FIELDS---')
	code, data = s_client.get_box_field(box_key)
	if(code == 200):
		for item in data:
			o = StreakField(**item)
			o.show()
			print("------------------")
	raw_input()
	print("---ONE FIELD---")
	code, data = s_client.get_box_field(box_key, o.attributes['key'])
	if(code == 200):
		o = StreakField(**data)
		o.show()
	print("------------------")
	raw_input()
	print('---ONE BOX, DELETE ALL FIELDS---')
	code, data = s_client.get_box_field(box_key)
	if(code == 200):
		for item in data:
			o = StreakField(**item)
			o.attributes['boxKey'] = box_key
			o.show()
			print("---Delete FIELD---")
			code, data = s_client.delete_box_field(o.attributes['pipelineKey'], o.attributes['key'])
			pprint(data)
			print("------------------")
	raw_input()
def newsfeed_api_test(s_client):
	box_key = 'agxzfm1haWxmb29nYWVyLwsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIEQ2FzZRjhxQgM'
	pipeline_key = 'agxzfm1haWxmb29nYWVyOAsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIIV29ya2Zsb3cYgICAgIDyiAoM'
	code, data = s_client.get_pipeline_newsfeeds(pipeline_key, "ALL")
	pprint("ALL PIPELINE NEWSFEED: {}".format(data))
	raw_input()
	code, data = s_client.get_pipeline_newsfeeds(pipeline_key, "CONDENSED")
	pprint("CONDENSED PIPELINE NEWSFEED: {}".format(data))
	raw_input()
	code, data = s_client.get_box_newsfeeds(box_key, "ALL")
	pprint("ALL BOX NEWSFEED: {}".format(data))
	raw_input()
	code, data = s_client.get_box_newsfeeds(box_key, "CONDENSED")
	pprint("CONDENSED BOX NEWSFEED: {}".format(data))
def threads_api_test(s_client):
	box_key = 'agxzfm1haWxmb29nYWVyLwsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIEQ2FzZRjhxQgM'
	print("---BOX THREADS---")
	code, data = s_client.get_box_threads(box_key)
	if code == 200:
		for item in data:
			o = StreakThread(**item)
			o.show()
			print("-------------")
	print("---ONE THREAD---")
	code, data = s_client.get_thread(o.attributes['key'])
	if code == 200:
		o = StreakThread(**data)
		o.show()
	print("-------------")
def comments_api_test(s_client):
	box_key = 'agxzfm1haWxmb29nYWVyLwsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIEQ2FzZRjhxQgM'
	print("---CREATE BOX COMMENT---")
	code, data = s_client.create_box_comments(box_key, "Hello World!")
	if code == 200:
		o = StreakComment(**data)
		o.show()
	print("------------------------")
	print("---GET BOX COMMENTS---")
	code, data = s_client.get_box_comments(box_key)
	if code == 200:
		for item in data:
			o = StreakComment(**item)
			o.show()
			#print(o.attributes['boxKey'], o.attributes['key'])
			#print("---DELETE BOX COMMENT---")
			#code, data = s_client.delete_box_comment(o.attributes['boxKey'], o.attributes['key'])
			#pprint(data)
			print("------------------------")
def files_api_test(s_client):
	box_key = 'agxzfm1haWxmb29nYWVyLwsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIEQ2FzZRjhxQgM'
	print("---GET BOX FILES---")
	code, data = s_client.get_box_files(box_key)
	if code == 200:
		for item in data:
			o = StreakFile(**item)
			o.show()
			#print(o.attributes['boxKey'], o.attributes['key'])
			#print("---DELETE BOX COMMENT---")
			#code, data = s_client.delete_box_comment(o.attributes['boxKey'], o.attributes['key'])
			#pprint(data)
			print("------------------------")
	print("---GET FILE---")
	code, data = s_client.get_file(o.attributes['fileKey'])
	if code == 200:
		o = StreakFile(**data)
		o.show()
	print("------------------------")
	print("---GET FILE LINK---")
	code, data = s_client.get_file_link(o.attributes['fileKey'])
	pprint(data)
	print("------------------------")
	print("---GET FILE CONTENTS---")
	code, data = s_client.get_file_contents(o.attributes['fileKey'])
	pprint(data)
	print("------------------------")
def box_reminder_api_test(s_client):
	import time
	box_key ='agxzfm1haWxmb29nYWVyLwsSDE9yZ2FuaXphdGlvbiIRbWVobWV0Z0BnbWFpbC5jb20MCxIEQ2FzZRjhxQgM'
	print('---ONE BOX, CREATE REMINDER---')
	code, data = s_client.create_box_reminder(box_key, 'hai!', str(int(time.time())+100000), True)
	if(code == 200):
		o = StreakReminder(**data)
		o.show()
	print("------------------")
	raw_input()
	print('---ONE BOX, CREATE REMINDER---')
	code, data = s_client.create_box_reminder(box_key, 'Moo!', str(int(time.time())+200000), False)
	if(code == 200):
		o = StreakReminder(**data)
		o.show()
	print("------------------")
	raw_input()
	print('---ONE BOX, ALL REMINDERS---')
	code, data = s_client.get_box_reminders(box_key)
	if(code == 200):
		for item in data:
			o = StreakReminder(**item)
			o.show()
			print("------------------")
	raw_input()
	print("---ONE REMINDER---")
	code, data = s_client.get_reminder(o.attributes['reminderKey'])
	if(code == 200):
		o = StreakReminder(**data)
		o.show()
	print("------------------")
	print("---UPDATE REMINDER---")
	o.attributes['message'] = "updated!"
	code, data = s_client.update_reminder(o)
	if(code == 200):
		o = StreakReminder(**data)
		o.show()
	print("------------------")
	raw_input()
	print('---ONE BOX, DELETE ALL REMINDERS---')
	code, data = s_client.get_box_reminders(box_key)
	if(code == 200):
		for item in data:
			o = StreakField(**item)
			o.show()
			print("---Delete Reminder---")
			code, data = s_client.delete_reminder(o.attributes['reminderKey'])
			pprint(data)
			print("------------------")
	raw_input()
	'''
def main():
	unittest.main(verbosity=2)

	'''
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(StreakClientTestUserAPI))
	unittest.TextTestRunner(verbosity=2).run(suite)
	'''
if __name__ == '__main__':
	main()
	
	
