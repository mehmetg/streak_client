import unittest
import sys
import os

if __name__ == '__main__':
	print "name", __name__
	sys.path.append(os.path.abspath(".."))
	from streak_client import *
else:
	print "name", __name__
	from ..streak_client import StreakClient


	key = '0b6359c686584bc3b610a640e2e7eb9f'



'''
class MyUptimeTest(unittest.TestCase):

	def setUp(self):
		self.system = platform.system()
		self.stdout_bkp = sys.stdout
		self.my_stdout = StringIO()

	def tearDown(self):
		#self.system = None
		self._clear_saved_stdout()

	def test_get_platform(self):
		self.assertTrue(my_uptime.get_platform() is self.system, 
						'Platform detection failed!')

	def test_uptime(self):
		r = re.compile(r'\d+:\d\d')
		self._redirect_stdout()
		my_uptime.uptime()
		self._restore_stdout()
		output = self._get_saved_stdout()
		
		if self.system == 'Linux':
			r = re.compile(r'.*\d\d:\d\d.\d+')
			system_response = ("System in use is %s" % self.system)
			lines = [line.strip() for line in output.split('\n')]
			if(len(lines) > 1):
				self.assertTrue(system_response == lines[0],
								"System type failed! \n%s !=  %s" % (lines[0] , system_response) )
				self.assertIsNotNone(r.match(lines[1]),
					"Uptime check failed on %s" % lines[1])
			else:
				self.assertTrue(False, 'Uptime output failed on %s' % self.system)
		else:
			correct_output = "%s is not supported!" % self.system
			self.assertTrue( correct_output == 
							 output.split('\n')[0].strip(),
							"Uptime on unsupported system failed!")

	def test_main(self):
		self._redirect_stdout()
		my_uptime.uptime()
		output1 = self._get_saved_stdout()
		self._clear_saved_stdout()
		my_uptime.main()
		output2 = self._get_saved_stdout()
		self._restore_stdout()
		self.assertEqual(output1, output2, "Main function does not behave same as uptime!")

	def  _redirect_stdout(self):
		sys.stdout = self.my_stdout

	def _restore_stdout(self):
		sys.stdout = self.stdout_bkp
	
	def _get_saved_stdout(self):
		return self.my_stdout.getvalue()

	def _clear_saved_stdout(self):
		return self.my_stdout.truncate(0)
'''
############
#Temporary test routines.
############
def user_api_test():
	print "name", __name__
	s_client = StreakClient(key)
	code, user_data = s_client.get_user()
	print('---ME---')
	user = StreakUser(**user_data)
	user.show()
	print('---USER BY ID---')
	code, user_data = s_client.get_user(user.attributes['userKey'])
	user = StreakUser(**user_data)
	user.show()
'''
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
	key = ''
	with open('/Users/mehmetgerceker/Desktop/bts/STREAK_API_KEY.txt','r') as f:
		key = f.read().strip()
	s_client = StreakClient(key)
	user_api_test(s_client)

if __name__ == '__main__':
	main()
	
	#suite = unittest.TestSuite()
	#suite.addTest(unittest.makeSuite(MyUptimeTest))
	#unittest.TextTestRunner(verbosity=2).run(suite)
