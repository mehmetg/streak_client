import sys
from setuptools import setup

__version__ = ''
with open('streak_client/__init__.py') as inp:
  for line in inp:
      if (line.startswith('__version__')):
          exec(line.strip())
          break

setup(	name='streak_client',
		version= __version__,
		description='simple flat client class for streak.com api with helper objects',
		long_description = 'Streak API Client in Python',
		url='http://github.com/mehmetg/streak_client',
		author='Mehmet Gerceker',
		author_email='mehmetg@msn.com',
		license='MIT',
		packages=['streak_client'],
		package_dir={'streak_client': 'streak_client'},
		keywords=( 'streak', 'api'),
		classifiers=[
	                 'Development Status :: 4 - Beta',
	                 'Topic :: Software Development :: Libraries :: Python Modules',
	                 'License :: OSI Approved :: MIT License',
	                 'Operating System :: MacOS',
	                 'Operating System :: Microsoft :: Windows',
	                 'Operating System :: POSIX',
	                 'Programming Language :: Python',
	                 'Programming Language :: Python :: 2',
	                 'Programming Language :: Python :: 3',
                	],
      	provides=[], 
      	install_requires=[ 'requests' ],
      	#message_extractors={},
      	#entry_points = {
      	#	'console_scripts': [
      	#		'streak_client = streak_client.streak_client:main',
      	#		'streak_client%s = streak_client.streak_client:main' % sys.version_info[0],
      	#	],
      	#	'distutil.commands': [
      	#		'streak_client = streak_client:main'
      	#	],
      	#},
		zip_safe=False,
		test_suite = 'streak_client_tests',
		#tests_require = [],
		#test_loader = '',
		)