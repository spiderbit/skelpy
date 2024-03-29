#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import shutil


def is_binary(filename):
	"""Return true iff the given filename is binary.

	Raises an EnvironmentError if the file does not exist or cannot be
	accessed.
	"""
	fin = open(filename, 'rb')
	try:
		CHUNKSIZE = 1024
		while 1:
			chunk = fin.read(CHUNKSIZE)
			if '\0' in chunk: # found null byte
				return True
			if len(chunk) < CHUNKSIZE:
				break # done
	finally:
		fin.close()
	return False

class SkelPy:
	def __init__(self):
		pass

	def init(self, path='.'):
		""" initialise and mark a diretory as a template """
		skel_path = os.path.join('.', path, '.skelpy')
		if os.path.exists(path):
			if not os.path.isdir(path):
				return 0
		if not os.path.exists(skel_path):
			os.makedirs(skel_path)

	def read_ignore_file(self, config_dir):
		ignore_path = os.path.join(config_dir, 'ignore')
		ignore_list = []
		if os.path.isfile(ignore_path):
			with open(ignore_path) as f:
				for line in f:
					ignore_list.append(line[:-1])
		return ignore_list


	def create(self, source, target):
		""" creates a new directory from the template """
		source = os.path.normpath(source)
		target = os.path.normpath(target)
		config_dir = os.path.join(source, '.skelpy')
		if os.path.isdir(config_dir):
			ignore_list = self.read_ignore_file(config_dir)
			if os.path.exists(target):
				if os.path.isdir(target):
					if os.listdir(target) == []:
						pass
					else:
						raise ValueError('target isnt empty, '+\
							'stopping to prevent data losts')
				else:
					raise NotImplementedError('...')
			else:
				os.mkdir(target)
			for root, dirs, files in os.walk(source):
				if root == source:
					dirs.remove('.skelpy')
				target_root = root.replace(source,target,1)
				#filter names
				target_root = target_root.replace('%project%', target)

				for d in dirs:
					for i in ignore_list:
						root2 = root.replace(source, '', 1)[1:]
						if os.path.join(root2, d).startswith(i):
							break
					else:
						d_renamed = d.replace('%project%', target)
						d_source = os.path.join(root, d)
						d_target = os.path.join(target_root, d_renamed)
						os.mkdir(d_target)
						shutil.copystat(d_source, d_target)
				for f in files:
					for i in ignore_list:
						root2 = root.replace(source, '', 1)[1:]
						if os.path.join(root2, f).startswith(i):
							break
					else:
						f_renamed = f.replace('%project%', target)
						f_source = os.path.join(root, f)
						f_target = os.path.join(target_root, f_renamed)
						with open(f_source, 'r') as f1:
							f_content = f1.read()
						f_content = f_content.replace('%project%', target)
						if is_binary(f_source):
							shutil.copy(f_source, f_target)
						else:
							with open(f_target, 'w+') as f2:
								f2.write(f_content)
