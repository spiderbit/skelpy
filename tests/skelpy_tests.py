from nose.tools import *
from os import environ as env
from skelpy.skelpy import SkelPy
import tempfile
import shutil
import os
from time import sleep

class Test_SkelPy(object):

	def setup(self):
		self.old_pwd = env['PWD']
		self.temp_dir = tempfile.mkdtemp()
		os.chdir(self.temp_dir)
		self.skel = SkelPy()

	def teardown(self):
		os.chdir(self.old_pwd)
		shutil.rmtree(self.temp_dir)

	def test_template_path_is_file(self):
		""" checks that a skelpy init dont override a file """
		with open('template1', 'w') as f:
				f.write('')
		assert os.path.isfile('template1')
		self.skel.init('template1')
		assert os.path.isfile('template1')

	def test_init_once(self):
		""" tests that the tool creates the template dir """
		self.skel.init('template1')
		skel_path = os.path.join(self.temp_dir, 'template1', '.skelpy')
		assert os.path.isdir(skel_path)

	def test_init_twice(self):
		""" tests that 2nd init call dont overrides the template dir """
		template_path = os.path.join(self.temp_dir, 'template1', '.skelpy')
		self.skel.init('template1')
		mod_time1 = os.path.getmtime(template_path)
		sleep(0.001)
		self.skel.init()
		mod_time2 = os.path.getmtime(template_path)
		assert mod_time1 == mod_time2

	def test_create_files_once(self):
		""" checks if create copies directories and files """
		self.skel.init('template1')
		os.chdir('template1')
		for path in 'a','b','c':
			os.mkdir(path)
			with open('file_%s' % path, 'w+') as f:
				f.write('0123456789abcdef')
			os.chdir(path)
		os.chdir(self.temp_dir)
		self.skel.init('template1')
		self.skel.create('template1', 'proj1')
		assert os.path.isdir('proj1')
		os.chdir('proj1')
		for path in 'a','b','c':
			files = os.listdir('.')
			assert set(files) == set([path, "file_"+path]), files
			assert os.path.isdir(path)
			assert os.path.isfile("file_%s" % path)
			f = open('file_%s' % path, 'r')
			assert '0123456789abcdef' == f.read(), f
			os.chdir(path)
