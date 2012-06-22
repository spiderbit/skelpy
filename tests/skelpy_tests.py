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

	def test_init_once(self):
		""" tests if the tool creates the template dir """
		self.skel.init()
		template_path = os.path.join(self.temp_dir, '.skelpy')
		assert os.path.isdir(template_path)

	def test_init_twice(self):
		""" tests that 2nd init call dont overrides the template dir """
		template_path = os.path.join(self.temp_dir, '.skelpy')
                self.skel.init()
		mod_time1 = os.path.getmtime(template_path)
		sleep(0.001)
		self.skel.init()
		mod_time2 = os.path.getmtime(template_path)
		assert mod_time1 == mod_time2

