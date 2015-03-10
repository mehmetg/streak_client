import unittest
import platform
import sys
import os
import re
	
if __name__ != '__main__':
	from my_uptime import my_uptime

if sys.version_info.major > 2:
	from io import StringIO
else:
	from StringIO import StringIO



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

if __name__ == '__main__':
	import imp
	
	#######
	module_dir = os.path.split(os.path.abspath(__file__))[0]
	module_dir = os.path.split(module_dir)[0]
	module_file = os.path.join(module_dir, 'my_uptime', 'my_uptime.py')
	print(module_file)
	my_uptime = imp.load_source('my_uptime', module_file)
	#######
	
	suite = unittest.TestSuite()
	suite.addTest(unittest.makeSuite(MyUptimeTest))
	unittest.TextTestRunner(verbosity=2).run(suite)
