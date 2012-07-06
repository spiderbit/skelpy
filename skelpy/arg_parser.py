#!/usr/bin/env python
#-*- coding:utf-8 -*-

from skelpy import SkelPy
import sys

class ArgParser(object):
	def __init__(self, args=sys.argv):
		self.args = args
		self.params = []
		self.skel = SkelPy()

	def parse(self):
		if self.args[1] == 'init':
			self.valid = True
			self.cmd = "init"
			self.params += self.args[2:]
		elif self.args[1] == 'create':
			self.valid = True
			self.cmd = "create"
			self.params += self.args[2:]

	def exec_cmd(self):
		if self.valid and self.cmd == "init":
			self.skel.init(self.params[0])
		elif self.valid and self.cmd == "create":
			self.skel.create(self.params[0], self.params[1])



