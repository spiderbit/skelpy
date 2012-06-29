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


	def create_sample_template(self, name):
		os.chdir(name)
		for path in 'a','b','c':
			os.mkdir(path)
			with open('file_%s' % path, 'w+') as f:
				f.write('0123456789abcdef')
			os.chdir(path)
		os.chdir(self.temp_dir)

	def test_create_copies_files(self):
		""" checks if create copies directories and files """
		name='template1'
		self.skel.init(name)
		self.create_sample_template(name)
		self.skel.create(name, 'proj1')
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

	def test_create_copies_only_from_templates(self):
		""" checks if create only accepts templates as source """
		name='template1'
		os.mkdir(name)
		self.create_sample_template(name)
		self.skel.create(name, 'proj1')
		assert not os.path.isdir('proj1')

	def check_files_exist(self, files):
		for i in files:
			files = os.listdir('.')
			d = i[0]
			f = i[1]
			if d == None:
				i.remove(None)
			if f == None:
				i.remove(None)
			assert set(files) == set(i), "%s vs %s" % (files, i)
			if d != None:
				assert os.path.isdir(d)
			if f != None:
				assert os.path.isfile(f)
			if d != None:
				os.chdir(d)

	def create_files(self, name, files):
		os.mkdir(name)
		os.chdir(name)
		for i in files:
			files = os.listdir('.')
			d = i[0]
			f = i[1]
			if d == None:
				i.remove(None)
			if f == None:
				i.remove(None)
			if d != None:
				os.mkdir(d)
			if f != None:
				with open(f, 'w') as fo:
					fo.write("")
			if d != None:
				os.chdir(d)
		os.chdir(self.temp_dir)

	def test_create_dont_copy_ignore_files(self):
		"""
		checks if create dont copy files and dirs listed in the .skelpy/ignore file
		"""
		name='template1'
		files =	[['a', 'file_a'],['b', 'file_b'],['c', 'file_c']]
		self.create_files(name, files)
		self.skel.init(name)
		ignore_file = os.path.join(name, '.skelpy', 'ignore')
		with open(ignore_file, 'w+') as f:
			file_b = os.path.join('a','file_b') + "\n"
			path_c = os.path.join('a','b','c') + "\n"
			f.write(file_b)
			f.write(path_c)
		self.skel.create(name, 'proj1')
		os.chdir('proj1')
		files =	[['a', 'file_a'],['b', None],[None, 'file_c']]
		self.check_files_exist(files)

	def test_create_renames_files_with_keyword(self):
		"""	checks that create renames dirs/files to proj-name """
		name='template1'
		files =	[['%project%', 'file_a'],['b', '%project%'],['%project%', 'file_c']]
		self.create_files(name, files)
		self.skel.init(name)
		self.skel.create(name, 'proj1')
		os.chdir('proj1')
		files =	[['proj1', 'file_a'],['b', 'proj1'],['proj1', 'file_c']]
		self.check_files_exist(files)


	def test_renames_strings_in_files_with_keyword(self):
		"""	checks that create renames strings in files to proj-name """
		#not yet implemented
		pass

	# maybe some tests for the cli client if it
	# calls the right methods with the right args
