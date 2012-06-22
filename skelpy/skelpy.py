#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os

class SkelPy:
	def __init__(self):
		pass

	def init(self):
		if not os.path.exists('.skelpy'):
			os.makedirs('.skelpy')
