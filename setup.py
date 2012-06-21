
#!/usr/bin/env python

name = "skelpy"

import versioneer
versioneer.versionfile_source = name+'/_version.py'
versioneer.versionfile_build = name+'/_version.py'
versioneer.tag_prefix = ''
versioneer.parentdir_prefix = name+'-'
import os
import sys

#from setuptools import setup
from distutils.core import setup

description='<short description>'
package_name = name


setup(name=name,
			version=versioneer.get_version(),
			cmdclass=versioneer.get_cmdclass(),
			description=description,
			author='Stefan Huchler',
			author_email='s.huchler@gmail.com',
			url='https://github.com/spiderbit/'+name,
			license='LICENSE',
			long_description=open('README').read(),
			packages = [package_name],
			py_modules = ['versioneer'],
			scripts=['bin/'+name]
			)
