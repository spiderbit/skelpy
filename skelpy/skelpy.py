#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import shutil

class SkelPy:
	def __init__(self):
		pass

	def init(self, path='.'):
		skel_path = os.path.join('.', path, '.skelpy')
		if os.path.exists(path):
			if not os.path.isdir(path):
				return 0
		if not os.path.exists(skel_path):
			os.makedirs(skel_path)

	def create(self, source, target):
		os.mkdir(target)
		for root, dirs, files in os.walk(source):
			target_root = root.replace(source,target,1)
			for d in dirs:
				if d != '.skelpy':
					d_source = os.path.join(root, d)
					d_target = os.path.join(target_root, d)
					os.mkdir(d_target)
					shutil.copystat(d_source, d_target)
			for f in files:
				f_source = os.path.join(root, f)
				f_target = os.path.join(target_root, f)
				shutil.copy(f_source, f_target)
